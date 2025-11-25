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
                echo 'Iniciando Pipeline Segura...'
            }
        }

        stage('Construcción (Build)') {
            steps {
                script {
                    echo '🔨 Construyendo imagen...'
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                    sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Despliegue (Deploy)') {
            steps {
                script {
                    echo '🚀 Desplegando aplicación...'
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                    
                    // Lanzamos la app en la red compartida
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
                    echo '🕵️ Ejecutando escaneo de vulnerabilidades...'

                    // 1. Aseguramos que la carpeta exista y esté limpia
                    sh "rm -rf zap_reports"
                    sh "mkdir -p zap_reports"
                    sh "chmod 777 zap_reports"

                    // 2. Ejecutamos ZAP como ROOT (-u 0) para evitar problemas de permisos
                    // Usamos 'zap-baseline-scan.py' primero, es más rápido y menos propenso a fallar por tiempos
                    sh """
                        docker run --rm \
                        -u 0 \
                        --network ${NETWORK_NAME} \
                        -v ${WORKSPACE}/zap_reports:/zap/wrk/:rw \
                        -t zaproxy/zap-stable \
                        zap-baseline-scan.py \
                        -t http://${CONTAINER_NAME}:5000 \
                        -r zap_report.html \
                        -I || true
                    """

                    // 3. Verificamos si el archivo se creó (para depuración)
                    sh "ls -l zap_reports/"
                }
            }
        }
    }

    // Esta sección se ejecuta siempre al final para guardar los archivos generados
    post {
        always {
            echo '📄 Archivando reportes de seguridad...'
            // Guardamos el reporte HTML para que puedas descargarlo desde Jenkins
            archiveArtifacts artifacts: 'zap_reports/zap_report.html', allowEmptyArchive: true
        }
    }
}