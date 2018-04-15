from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

response.download(dict(
    keywords="gazprom logo",
    format='jpg',
    limit=30
))
