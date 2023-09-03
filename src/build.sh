branch=`git rev-parse --abbrev-ref HEAD`
docker build -t rbrandstaedter/solarflow-statuspage:$branch .

docker image push rbrandstaedter/solarflow-statuspage:$branch