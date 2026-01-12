pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "rvorbita/mini_shop"
        DOCKER_TAG = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                git branch: 'main', credentialsId: 'github-creds', url: 'https://github.com/rvorbita/mini_shop.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                """
            }
        }

        stage('Test Docker Image') {
            steps {
                sh """
                    docker rm -f test_app || true
                    docker run -d -p 5001:5001 --name test_app ${DOCKER_IMAGE}:${DOCKER_TAG}
                    sleep 5
                    curl -f http://localhost:5001 || exit 1
                    docker rm -f test_app
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_PASS')]) {
                    sh """
                        echo $DOCKER_PASS | docker login -u rvorbita --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                }
            }
        }

        stage('Deploy to k3s') {
            steps {
                withCredentials([file(credentialsId: 'k3s-config', variable: 'KUBECONFIG')]) {
                    sh """
                        export KUBECONFIG=$KUBECONFIG
                        
                        # Apply Kubernetes manifests
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml

                        # Optional: rollout status to wait until deployment is ready
                        kubectl rollout status deployment/mini-shop
                    """
                }
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed! Check the logs above for details."
        }
        success {
            echo "Pipeline succeeded! Your mini-shop app is deployed to k3s."
        }
    }
}
