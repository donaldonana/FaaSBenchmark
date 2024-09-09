
wsk action update decode  --memory 200 --docker onanad/action-python-v3.9:decode decode/__main__.py --web true 

wsk action update draw    --memory 128 --docker onanad/action-python-v3.9:draw   draw/__main__.py --web true 

wsk action update encode  --memory 128 --docker onanad/action-python-v3.9:encode encode/__main__.py --web true 

wsk action update facerec --memory 256 --docker onanad/action-python-v3.9:facerec facial/__main__.py --web true 

wsk action update facerecprim --memory 300 --docker onanad/action-python-v3.9:facerecprim facial-prim/__main__.py --web true 

wsk action update keep --memory 200 --docker onanad/action-python-v3.9:keep keep-scene/__main__.py --web true 

wsk action update scenechange --memory 200 --docker onanad/action-python-v3.9:scenechange scene-change/__main__.py --web true 
