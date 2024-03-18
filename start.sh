docker network create --opt com.docker.network.driver.mtu=1500 my-restricted-network
docker network policy create --ingress --from none my-restricted-policy
docker network policy rule add my-restricted-policy --from my-restricted-network --to any --port any --protocol tcp --action deny
docker network policy rule add my-restricted-policy --from my-restricted-network --to any --port any --protocol udp --action deny
docker network policy rule add my-restricted-policy --from my-restricted-network --to any --port 5000 --protocol tcp --action allow  # Allow access to localhost port 5000 (HTTP)