pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        ENV_FILE = '.env'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Stop Existing Containers') {
            steps {
                script {
                    echo 'Stopping existing containers...'
                    sh '''
                        # Force stop and remove containers by name if they exist
                        docker stop myauxilium_backend myauxilium_mysql 2>/dev/null || true
                        docker rm myauxilium_backend myauxilium_mysql 2>/dev/null || true
                        
                        # Then run docker-compose down to clean up networks and volumes
                        docker-compose down --remove-orphans || true
                    '''
                }
            }
        }
        
        stage('Write .env file') {
            steps {
                script {
                    echo 'Writing .env file from Jenkins credentials...'
                    
                    // Get the entire .env file content from Jenkins credentials
                    withCredentials([
                        string(credentialsId: 'vela-back-end-env', variable: 'BACK_END_ENV')
                    ]) {
                        sh '''
                            echo "$BACK_END_ENV" > .env
                            echo "Environment file created:"
                            cat .env
                        '''
                    }
                }
            }
        }
                
        stage('Build') {
            steps {
                script {
                    echo 'Building containers...'
                    
                    // Build the containers with the .env file already present
                    sh 'docker-compose build --no-cache'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    echo 'Starting containers...'
                    
                    // Start the services - the .env file is already in place
                    sh 'docker-compose up -d'
                    
                    // Wait for services to be ready
                    sh 'sleep 30'
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    sh 'sleep 10'
                    sh 'curl -f http://localhost:8000/health-check || echo "Health check failed, but continuing..."'
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    sh 'docker image prune -f'
                }
            }
        }
    }
    
    post {
        always {
            script {
                sh 'docker-compose ps'
            }
        }
        
        failure {
            script {
                sh 'docker-compose down'
            }
        }
    }
} 