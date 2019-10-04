# keiba-ataru
競馬予測サイトのbackend
frontは[こちら](https://github.com/shwan01/keiba-app-frontend)

keyword : Django REST framework, Swagger, ML, tpot, Docker
## docs
- docs/swagger.yml  
    drf-yasgでauto-generateしたyml
## 環境構築
```
docker-compose -f "keiba-ataru-backend/docker-compose.yml" up -d --build

# サーバー立ち上げ
docker exec -it keiba-ataru-backend_api_[0-9] python3 api/manage.py runserver 0.0.0.0:8000
```