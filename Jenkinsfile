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
                    sh 'docker-compose -f docker-compose.yml down --remove-orphans'
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
                        '''
                    }
                }
            }
        }
                
        stage('Build') {
            steps {
                script {
                    echo 'Building containers...'
                    
                    // Build the containers
                    sh 'docker-compose build --no-cache'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    echo 'Starting containers...'
                    
                    // Start the services
                    sh 'docker-compose up -d'
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo 'Performing health checks...'
                    
                    // Wait for services to be ready
                    sh 'sleep 30'
                    
                    // Check if the backend is responding
                    sh '''
                        for i in {1..10}; do
                            if curl -f http://localhost:8000/health-check; then
                                echo "Backend is healthy!"
                                break
                            else
                                echo "Attempt $i: Backend not ready yet..."
                                sleep 10
                            fi
                        done
                    '''
                    
                    // Check if MySQL is healthy
                    sh '''
                        for i in {1..10}; do
                            if docker-compose exec -T mysql mysqladmin ping -h localhost --silent; then
                                echo "MySQL is healthy!"
                                break
                            else
                                echo "Attempt $i: MySQL not ready yet..."
                                sleep 10
                            fi
                        done
                    '''
                }
            }
        }

        stage('Database Migration') {
            steps {
                script {
                    echo 'Performing database migrations...'
                    
                    // 1. Erase the content of the folder alembic/versions
                    sh '''
                        echo "Clearing alembic/versions folder..."
                        rm -rf alembic/versions/*
                        echo "alembic/versions folder cleared"
                    '''
                    
                    // 2. Log into mysql and erase the content of the table "alembic_version"
                    sh '''
                        echo "Clearing alembic_version table..."
                        mysql -h localhost -P 3306 -u root -p rootpassword myauxilium -e "DELETE FROM alembic_version;"
                        echo "alembic_version table cleared"
                    '''
                    
                    // 3a. Generate new migration
                    sh '''
                        echo "Generating new migration..."
                        alembic -c alembic.ini revision --autogenerate -m "Automated migration"
                        echo "Migration generated successfully"
                    '''
                    
                    // 3b. Apply migration
                    sh '''
                        echo "Applying migration..."
                        alembic -c alembic.ini upgrade head
                        echo "Migration applied successfully"
                    '''
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    echo 'Cleaning up...'
                    // Remove unused images to save space
                    sh 'docker image prune -f'
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo 'Deployment completed!'
                
                // Show running containers
                sh 'docker-compose ps'
                
                // Show logs if there are any issues
                sh 'docker-compose logs --tail=50'
            }
        }
        
        failure {
            script {
                echo 'Deployment failed! Rolling back...'
                
                // Stop all containers
                sh 'docker-compose down'
                
                // Send notification (you can customize this)
                echo 'Deployment failed - containers stopped'
            }
        }
        
        success {
            script {
                echo 'Deployment successful!'
                
                // You can add notifications here (email, Slack, etc.)
                echo 'Application is now running on http://localhost:8000'
            }
        }
    }
} 