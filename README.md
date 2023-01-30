# coppelTest
Repository for coppel python backend skills test

Postman collection: coppel.postman_collection.json
Docker commands:

    docker run -d --name  test1_container --net=bridge -p 3000:3000  test1_image
    
    docker run -d --name  test2_container --net=bridge -p 3001:3001  test2_image 
    
    docker run -d --name  test3_container --net=bridge -e USERS_ENDPOINT='http://{DOCKER_IP_TEST2}:3001/
    users' -e COMICS_ENDPOINT='http://{DOCKER_IP_TEST1}:3000/searchComics/' -p 3002:3002  test3_image 
    
    docker run -d --name  test4_container --net=bridge -e USERS_ENDPOINT=‘http://{DOCKER_IP_TEST2}:3001/users' -p 3003:3003  test4_image
