pipeline {
    agent {
        label 'nominaflow-ci'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment') {
            steps {
                sh '''
                    echo "Python version:"
                    python3 --version

                    echo "Pip version:"
                    pip3 --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv /tmp/nominaflow-ci-venv
                    /tmp/nominaflow-ci-venv/bin/python -m pip install --upgrade pip
                    /tmp/nominaflow-ci-venv/bin/pip install ".[dev]"
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    mkdir -p reports

                    /tmp/nominaflow-ci-venv/bin/pytest \
                        --junitxml=reports/junit.xml \
                        --cov=src \
                        --cov-report=xml:reports/coverage.xml \
                        --cov-report=term
                '''
            }
        }
    }

    post {
        always {
            junit 'reports/junit.xml'

            archiveArtifacts(
                artifacts: 'reports/coverage.xml',
                allowEmptyArchive: true
            )
        }

        success {
            echo 'NominaFlow CI: Tests passed successfully.'
        }

        failure {
            echo 'NominaFlow CI: Pipeline failed. Check the test results and console output.'
        }

        cleanup {
            sh 'rm -rf /tmp/nominaflow-ci-venv'
        }
    }
}