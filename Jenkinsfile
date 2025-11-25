// Integrantes: Diego Henríquez y
// Sección: OCY1102


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
                // RECUERDA: Cambiar NOMBRE_INTEGRANTE por tu nombre real
                echo 'Iniciando Pipeline - Integrante: NOMBRE_INTEGRANTE' 
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
                    echo '⏳ Esperando 10 segundos para que la app inicie...'
                    sleep 10
                    
                    echo '🕵️ Preparando directorios...'
                    sh "rm -rf zap_reports"
                    sh "mkdir -p zap_reports"
                    sh "chmod 777 zap_reports"

                    echo '🔥 Ejecutando ZAP Baseline Scan...'
                    
                    // CORRECCIÓN FINAL:
                    // 1. Usamos /zap/zap-baseline.py (que ya verificamos que existe)
                    // 2. En el flag -r, ponemos /zap/wrk/zap_report.html para obligarlo a guardar en el volumen compartido
                    sh """
                        docker run --rm \
                        -u 0 \
                        --network ${NETWORK_NAME} \
                        -v ${WORKSPACE}/zap_reports:/zap/wrk/:rw \
                        -t zaproxy/zap-stable \
                        /zap/zap-baseline.py \
                        -t http://${CONTAINER_NAME}:5000 \
                        -r /zap/wrk/zap_report.html \
                        -I || true
                    """
                }
            }
        }
    }

    post {
        always {
            echo '📄 Archivando reporte...'
            archiveArtifacts artifacts: 'zap_reports/zap_report.html', allowEmptyArchive: true
        }
    }
}