pipeline {
    agent any

    environment {
        IMAGE_NAME = "vulnerable-app"
        CONTAINER_NAME = "vulnerable-app-container"
        NETWORK_NAME = "red-ciberseguridad"
    }

    stages {
        stage('Inicio') {
            steps {
                echo 'Iniciando Pipeline de Depuración...'
            }
        }

        stage('Construcción (Build)') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                    sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Despliegue (Deploy)') {
            steps {
                script {
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"

                    sh """
                        docker run -d \
                        --name ${CONTAINER_NAME} \
                        --network ${NETWORK_NAME} \
                        -p 5001:5000 \
                        ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Pentesting (OWASP ZAP)') {
            steps {
                script {
                    echo '⏳ Esperando 20 segundos para que la app inicie correctamente...'
                    sleep 20

                    echo '🕵️ Preparando directorios...'
                    sh "rm -rf zap_reports"
                    sh "mkdir -p zap_reports"
                    sh "chmod 777 zap_reports"

                    echo '🔥 Iniciando escaneo (sin ocultar errores)...'
                    // NOTA: He quitado el "|| true" para ver el error real en la consola
                    sh """
                        docker run --rm \
                        -u 0 \
                        --network ${NETWORK_NAME} \
                        -v ${WORKSPACE}/zap_reports:/zap/wrk/:rw \
                        -t zaproxy/zap-stable \
                        zap-baseline-scan.py \
                        -t http://${CONTAINER_NAME}:5000 \
                        -r zap_report.html
                    """
                }
            }
        }
    }

    post {
        failure {
            script {
                echo '❌ El escaneo falló. Mostrando logs de la aplicación para depurar:'
                sh "docker logs ${CONTAINER_NAME}"
            }
        }
        always {
            archiveArtifacts artifacts: 'zap_reports/zap_report.html', allowEmptyArchive: true
        }
    }
}