import pytest
from fastapi.testclient import TestClient
from app.main import * 

def test_translate(authorized_client):
    client = authorized_client
    ok = {"text":"Bonjour"}
    # 200 status for valid body 
    ok_response = client.post("/translation", json=ok)
    assert ok_response.status_code == 200
    assert [i for i in ok_response.json().keys()] == ['text','translation']

    # status code 422 for invalid body requests
    key_err = {"tet": "Bonjour"}
    key_err_response = client.post("/translation", json=key_err)
    assert key_err_response.status_code == 422
    text_num = {"text":42}
    text_num_response = client.post("/translation", json=text_num)
    assert key_err_response.status_code == 422
    text_empty = {}
    text_empty_response = client.post("/translation", json=text_empty)
    assert text_num_response.status_code == 422
    text_list = {"text":["Holy Moly","Guten Tag"]}
    text_list_response = client.post("/translation", json=text_list)
    assert text_num_response.status_code == 422
    len_text = {"text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit.Ut velit mauris, egestas sed, gravida nec, ornare ut, mi. Aenean ut orci vel massa suscipit pulvinar. Nulla sollicitudin. Fusce varius, ligula non tempus aliquam, nunc turpis ullamcorper nibh, in tempus sapien eros vitae ligula. Pellentesque rhoncus nunc et augue. Integer id felis. Curabitur aliquet pellentesque diam. Integer quis metus vitae elit lobortis egestas. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Morbi vel erat non mauris convallis vehicula. Nulla et sapien. Integer tortor tellus, aliquam faucibus, convallis id, congue eu, quam. Mauris ullamcorper felis vitae erat. Proin feugiat, augue non elementum posuere, metus purus iaculis lectus, et tristique ligula justo vitae magna.Aliquam convallis sollicitudin purus. Praesent aliquam, enim at fermentum mollis, ligula massa adipiscing nisl, ac euismod nibh nisl eu lectus. Fusce vulputate sem at sapien. Vivamus leo. Aliquam euismod libero eu enim. Nulla nec felis sed leo placerat imperdiet. Aenean suscipit nulla in justo. Suspendisse cursus rutrum augue. Nulla tincidunt tincidunt mi. Curabitur iaculis, lorem vel rhoncus faucibus, felis magna fermentum augue, et ultricies lacus lorem varius purus. Curabitur eu amet."}
    text_len_response = client.post("/translation", json=len_text)
    assert text_len_response.status_code == 422


def test_feedback(authorized_client):
    client = authorized_client
    # it works 
    ok = {"text":"Bonjour","translation":"Dzien dobry","is_correct":"True"}
    k_response = client.post("translation/feedback", json=ok)
    assert k_response.status_code == 201

    # 0 or 1 should count as boolean
    is_correct_smallint = {"text":"efgrgrr","translation":"egeeeezf","is_correct":1}
    response = client.post("translation/feedback", json=is_correct_smallint)
    assert response.status_code == 201
    # ! + check if indeed created

    # Empty string should be counted as invalid
    empty_text = {"text":"","translation":"feeihfiofe","is_correct":"True"}
    response = client.post("translation/feedback", json=empty_text)
    assert response.status_code == 422

    empty_translation = {"text":"efgrgrr","translation":"","is_correct":"True"}
    response = client.post("translation/feedback", json=empty_translation)
    assert response.status_code == 422 
    # Field missing
    key_miss = {"translation":"feeihfiofe","is_correct":"True"}
    response = client.post("translation/feedback", json=key_miss)
    assert response.status_code == 422 

    # Wrong datatype
    datatype_text = {"text":["Bonjour"],"translation":"Dzien dobry","is_correct":"True"}
    response = client.post("translation/feedback", json=datatype_text)
    assert response.status_code == 422 
    datatype_tanslation = {"text":"sdjnefef","translation":42,"is_correct":"True"}
    response = client.post("translation/feedback", json=datatype_tanslation)
    assert response.status_code == 422 
    datatype_is_coorect = {"text":"efgrgrr","translation":"QEFfefefee","is_correct":"djnekjefn"}
    response = client.post("translation/feedback", json=datatype_is_coorect)
    assert response.status_code == 422 


    more_characters  = "be48c6269a1c3eca267bd09892eb369c6c000e4c36fb151f6ad6ad96d6a7e3e0555d51ee0609b21ed026ce84ef7515999d52f70d1f501243654f16eea71149ff3f261913bffbb62c48bf789904a000c77449ff1d3a1c66143e906fd6982bae5559e52b0024bcc4b43e7c287f599995381b8b838da9fb05c14d1a75691c8460ff020b70c6da3e9a8535724651c5cf2020004bb69bd9d6802f88d21209d2b81ddf55536fa5bdc92272287c068a02f99935f8ac402be9b46ed3d4335af9d7c632ff"
    overlength_text = {"text":more_characters,"translation":"fzehfr","is_correct":"True"}
    response = client.post("translation/feedback", json=overlength_text)
    assert response.status_code == 422 
    overlength_translation = {"text":"eahfofnef","translation":more_characters,"is_correct":"True"}
    response = client.post("translation/feedback", json=overlength_translation)
    assert response.status_code == 422 

