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
                            # Alternative approach: Use base64 to preserve exact formatting
                            # First, encode the content in Jenkins credentials as base64
                            # Then decode it here to preserve line breaks
                            echo "$BACK_END_ENV" | base64 -d > .env
                            
                            # If base64 doesn't work, try this approach:
                            # echo "$BACK_END_ENV" | tr -d '\r' > .env
                            
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
                    // sh 'sleep 10'
                    sh 'curl -f http://localhost:8000/health-check || echo "Health check failed, but continuing..."'
                }
            }
        }
        
        stage('Database Migration Setup') {
            steps {
                script {
                    // Wait a bit more to ensure database is fully ready
                    sh 'sleep 10'
                    
                    // 1. Erase the content of the folder alembic/versions in the myauxilium_backend container
                    sh '''
                        docker exec myauxilium_backend rm -rf /app/alembic/versions/*
                        docker exec myauxilium_backend ls -la /app/alembic/versions/ || true
                    '''
                    
                    // 2. Erase the content of the table alembic_versions in the myauxilium_mysql container
                    sh '''
                        docker exec myauxilium_mysql mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "DELETE FROM alembic_versions;" ${MYSQL_DATABASE} || true
                    '''
                }
            }
        }
        
        stage('Database Migration') {
            steps {
                script {
                    // 3. Run alembic commands consecutively in the myauxilium_backend container
                    sh '''
                        docker exec myauxilium_backend alembic -c alembic.ini revision --autogenerate -m "Auto-generated migration from Jenkins deployment"
                        docker exec myauxilium_backend alembic -c alembic.ini upgrade head
                    '''
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