pipeline {
  agent any

  stages {

    stage('Test GitHub Access') {
      steps {
        echo "Testing GitHub checkout..."
        git credentialsId: 'github-creds',
            url: 'https://github.com/rvorbita/mini_shop.git'
        sh 'ls -la'
      }
    }

    stage('Test k3s Access') {
      steps {
        withCredentials([file(credentialsId: 'k3s-config', variable: 'KUBECONFIG')]) {
          sh '''
            export KUBECONFIG=$KUBECONFIG
            kubectl get nodes
            kubectl get pods -A
          '''
        }
      }
    }
  }
}
