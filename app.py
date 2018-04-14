import mrrest

from aiohttp import web
from datetime import datetime

from db import db


async def search(request):
    query = request.rel_url.query

    try:
        faces = list(set(x.strip().lower() for x in query.get('faces', '').split(',') if x.strip()))
        logos = list(set(x.strip().lower() for x in query.get('logos', '').split(',') if x.strip()))

        phrases = list(set(x.strip().lower() for x in query.get('phrases', '').split(',') if x.strip()))

        # presents = [x.strip().lower() for x in query.get('presents', '').split(',') if x.strip()]
    except KeyError as err:
        raise web.HTTPBadRequest(text=str(err).strip('"'))

    predicates = []
    if faces or logos:
        is_feature_using = True

        for face in faces:
            predicates.append(f"f.image = 'face' AND f.info -> 'name' = '{face}'")

        for logo in logos:
            predicates.append(f"f.image='logo' AND f.info -> 'name' = '{logo}'")
    else:
        is_feature_using = False

    if phrases:
        is_dubbing_using = True

        for phrase in phrases:
            predicates.append(f"d.text ILIKE '%%{phrase}%%'")
    else:
        is_dubbing_using = False

    if is_feature_using and (not is_dubbing_using):
        search_query = '''
        SELECT
            f.video_id,
            f.frames[1] as start,
            f.frames[2] as finish,
            (SELECT sum(s :: INT)
             FROM unnest(ARRAY [
             {predicates}
             ]) s) AS weight
        FROM feature f
            INNER JOIN video v
                ON f.video_id = v.id
        '''
    elif (not is_feature_using) and is_dubbing_using:
        search_query = '''
        SELECT
            d.video_id,
            d.frames[1] as start,
            d.frames[2] as finish,
            (SELECT sum(s :: INT)
             FROM unnest(ARRAY [
             {predicates}
             ]) s) AS weight
        FROM dubbing d
            INNER JOIN video v
                ON d.video_id = v.id
        '''
    elif is_feature_using and is_dubbing_using:
        search_query = '''
        SELECT
            f.video_id,
            least(f.frames[1], d.frames[1]) as start,
            greatest(f.frames[2], d.frames[2]) as finish,
            (SELECT sum(s :: INT)
             FROM unnest(ARRAY [
             {predicates}
             ]) s) AS weight
        FROM feature f
            INNER JOIN dubbing d
                ON f.video_id = d.video_id
                   AND (f.frames [1] - {d} < d.frames [2] + {d} OR d.frames [1] - {d} < f.frames [2] + {d})
            INNER JOIN video v
                ON f.video_id = v.id
        '''
    else:
        raise web.HTTPBadRequest(text='no goals for search')

    query = """
    SELECT
        video_id,
        min(start) as start,
        min(finish) as finish
    FROM ( {sbuq} ) t
    WHERE weight > 0
    GROUP BY video_id
    ORDER BY count(video_id) DESC, sum(weight)/count(video_id) DESC
    """.format(sbuq=search_query).format(
        d=10,
        predicates=', '.join(predicates)
    )

    print(query)
    res = [
        {
            'video_id': row[0],
            'start': row[1],
            'finish': row[2]
        } for row in db.execute_sql(query).fetchall()
    ]

    return res

api = mrrest.RESTApi(
    '0.0.0.0',
    8000,
    routes=[
        web.get('/', lambda r: 'Service is available\n{}'.format(datetime.now())),
        web.get('/search', search)
    ]
)

api.run()
