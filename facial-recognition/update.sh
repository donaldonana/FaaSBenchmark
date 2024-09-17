
docker pull onanad/action-python-v3.9:decode
wsk action update decode  --memory 200 --docker onanad/action-python-v3.9:decode decode/__main__.py --web true 

docker pull onanad/action-python-v3.9:draw
wsk action update draw    --memory 128 --docker onanad/action-python-v3.9:draw   draw/__main__.py --web true 

docker pull onanad/action-python-v3.9:encode
wsk action update encode  --memory 300 --docker onanad/action-python-v3.9:encode encode/__main__.py --web true 

docker pull onanad/action-python-v3.9:facerec
wsk action update facerec --memory 256 --docker onanad/action-python-v3.9:facerec facial/__main__.py --web true 

docker pull onanad/action-python-v3.9:facerecprim
wsk action update facerecprim --memory 300 --docker onanad/action-python-v3.9:facerecprim facial-prim/__main__.py --web true

docker pull onanad/action-python-v3.9:keep
wsk action update keep --memory 200 --docker onanad/action-python-v3.9:keep keep-scene/__main__.py --web true 

docker pull onanad/action-python-v3.9:scenechange
wsk action update scenechange --memory 200 --docker onanad/action-python-v3.9:scenechange scene-change/__main__.py --web true 
