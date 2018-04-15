import json

from db import db

video_id = 0

json_file = json.load(open('/Users/i2rdt/Downloads/facts (2).json'))
frames = json_file['facts']

curr = 0

runs = []
run = {}
for no, facts in frames:
    # facts = list(set(facts))
    while curr < no:
        for fact in facts:
            pos = fact['coordinates']
            tpe = fact['type']
            name = fact.get('info', {}).get('name', '')

            query = '''
            INSERT INTO feature (video_id, pos, image, frames, info) VALUES
              ({video_id}, '{pos[0][0]}, {pos[0][1]}, {pos[1][0]}, {pos[1][1]}'::BOX, '{tpe}', ARRAY[{curr}, {curr}], 'name => "{name}"'::hstore)
            '''.format(
                video_id=video_id,
                pos=pos,
                tpe=tpe,
                curr=curr,
                name=name
            )
            print(query)

            db.execute_sql(query)

        print()
        last_facts = facts
        curr += 1

