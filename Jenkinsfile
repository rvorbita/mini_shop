pipeline {
  agent any

  environment {
    IMAGE_NAME = "rvorbita/mini_shop"
    IMAGE_TAG  = "${BUILD_NUMBER}"
  }

  stages {

    stage('Checkout') {
      steps {
        cleanWs()
        git branch: 'main', credentialsId: 'github-creds',
            url: 'https://github.com/rvorbita/mini_shop.git'
      }
    }

    stage('Build Image') {
      steps {
        sh '''
          docker build -t $IMAGE_NAME:$IMAGE_TAG .
          docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
        '''
      }
    }

    stage('Test Image') {
      steps {
        sh '''
          docker rm -f test_app || true
          docker run -d -p 5001:5001 --name test_app $IMAGE_NAME:$IMAGE_TAG
          sleep 5
          curl -f http://localhost:5001
          docker rm -f test_app
        '''
      }
    }

    stage('Push to Registry') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'dockerhub-creds',
          usernameVariable: 'DOCKER_USER',
          passwordVariable: 'DOCKER_PASS'
        )]) {
          sh '''
            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
            docker push $IMAGE_NAME:$IMAGE_TAG
            docker push $IMAGE_NAME:latest
          '''
        }
      }
    }

    stage('Deploy to k3s') {
      steps {
        withCredentials([file(credentialsId: 'k3s-config', variable: 'KUBECONFIG')]) {
          sh '''
            export KUBECONFIG=$KUBECONFIG

            # Apply all Kubernetes manifests
            kubectl apply -f k8s/

            # Wait for Postgres to be ready
            kubectl rollout status deployment/mini-shop-db

            # Run bootstrap_admin as a Job
            kubectl apply -f k8s/bootstrap-admin-job.yaml

            # Deploy/Update mini-shop app
            kubectl rollout status deployment/mini-shop
          '''
        }
      }
    }
  }
}
