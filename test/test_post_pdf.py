from src.webserver import create_app
from src.samples.cv import body
from src.cvreader import CvReader
import json
def setup():
    app = create_app()
    client = app.test_client()
    return client

def test_post_pdf_should_return_postulant_info():
    client = setup()
    user_data = {
        "cv":body,
        "requirements": {
            "knowledges":["python","flask","java"],
            "soft":["alegre","listo","trabajador"],
            "education":["Bootcamp","Bachelor","Master"]
        },
    }
    response = client.post("/api/v1/cv", data=json.dumps(user_data), content_type="application/json")

    assert response.json == {
        "knowledges":["Flask","Python"],
        "soft":["alegre"],
        "education":["BOOTCAMP"],
        "compatibility":80
    }