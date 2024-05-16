import pytest
from fastapi.testclient import TestClient
from app.main import * 


@pytest.fixture(scope="function")
def client():
    yield TestClient(app)

def test_translate(client):
    ok = {"text":"Bonjour"}

    # 200 status for valid body 
    ok_response = client.post("/translate", json=ok)
    assert ok_response.status_code == 200
    assert [i for i in ok_response.json().keys()] == ['text','translation']

    # status code 422 for invalid body requests
    key_err = {"tet": "Bonjour"}
    key_err_response = client.post("/translate", json=key_err)
    assert key_err_response.status_code == 422
    text_num = {"text":42}
    text_num_response = client.post("/translate", json=text_num)
    assert key_err_response.status_code == 422
    text_empty = {}
    text_empty_response = client.post("/translate", json=text_empty)
    assert text_num_response.status_code == 422
    text_list = {"text":["Holy Moly","Guten Tag"]}
    text_list_response = client.post("/translate", json=text_list)
    assert text_num_response.status_code == 422
    len_text = {"text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit.Ut velit mauris, egestas sed, gravida nec, ornare ut, mi. Aenean ut orci vel massa suscipit pulvinar. Nulla sollicitudin. Fusce varius, ligula non tempus aliquam, nunc turpis ullamcorper nibh, in tempus sapien eros vitae ligula. Pellentesque rhoncus nunc et augue. Integer id felis. Curabitur aliquet pellentesque diam. Integer quis metus vitae elit lobortis egestas. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Morbi vel erat non mauris convallis vehicula. Nulla et sapien. Integer tortor tellus, aliquam faucibus, convallis id, congue eu, quam. Mauris ullamcorper felis vitae erat. Proin feugiat, augue non elementum posuere, metus purus iaculis lectus, et tristique ligula justo vitae magna.Aliquam convallis sollicitudin purus. Praesent aliquam, enim at fermentum mollis, ligula massa adipiscing nisl, ac euismod nibh nisl eu lectus. Fusce vulputate sem at sapien. Vivamus leo. Aliquam euismod libero eu enim. Nulla nec felis sed leo placerat imperdiet. Aenean suscipit nulla in justo. Suspendisse cursus rutrum augue. Nulla tincidunt tincidunt mi. Curabitur iaculis, lorem vel rhoncus faucibus, felis magna fermentum augue, et ultricies lacus lorem varius purus. Curabitur eu amet."}
    text_len_response = client.post("/translate", json=len_text)
    assert text_len_response.status_code == 422

