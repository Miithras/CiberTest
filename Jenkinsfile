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
                    
                    // Creamos un directorio para reportes y damos permisos
                    sh "mkdir -p zap_reports"
                    sh "chmod 777 zap_reports"

                    // Ejecutamos ZAP usando Docker
                    // -v ${WORKSPACE}/zap_reports:/zap/wrk/:rw -> Mapeamos carpeta para guardar el reporte
                    // -t http://${CONTAINER_NAME}:5000 -> Atacamos al contenedor por su nombre interno
                    // -r zap_report.html -> Nombre del reporte
                    // || true -> Importante: Evita que el Pipeline se detenga si encuentra alertas (queremos ver el reporte)
                    sh """
                        docker run --rm \
                        --network ${NETWORK_NAME} \
                        -v ${WORKSPACE}/zap_reports:/zap/wrk/:rw \
                        -t zaproxy/zap-stable \
                        zap-full-scan.py \
                        -t http://${CONTAINER_NAME}:5000 \
                        -r zap_report.html \
                        -I || true
                    """
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