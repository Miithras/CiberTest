// Integrantes: Diego Henríquez
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
                echo 'Iniciando Pipeline Final - Integrante: Diego Henríquez' 
            }
        }

        stage('Construcción (Build)') {
            steps {
                script {
                    echo '🔨 Construyendo imagen...'
                    // Mantenemos --no-cache para asegurar actualizaciones
                    sh "docker build --no-cache -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
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
                    
                    // IMPORTANTE: debug=False para que funcionen las métricas y Flask sea estable
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
                    echo '⏳ Esperando 10 segundos para inicio...'
                    sleep 10
                    
                    // Limpieza previa
                    sh "rm -rf zap_reports"
                    sh "mkdir -p zap_reports"
                    sh "docker rm -f zap-scanner || true"

                    echo '🔥 Ejecutando ZAP Scan...'
                    // Usamos full-scan como pediste
                    sh """
                        docker run \
                        --name zap-scanner \
                        --network ${NETWORK_NAME} \
                        -u 0 \
                        -v /zap/wrk \
                        -t zaproxy/zap-stable \
                        /zap/zap-full-scan.py \
                        -t http://${CONTAINER_NAME}:5000 \
                        -r zap_report.html \
                        -I || true
                    """
                    
                    echo '📥 Extrayendo reporte ZAP...'
                    sh "docker cp zap-scanner:/zap/wrk/zap_report.html ./zap_reports/zap_report.html"
                    sh "docker rm zap-scanner"
                }
            }
        }

        stage('Análisis de Dependencias (Dependency Check)') {
            steps {
                script {
                    echo '🔍 Analizando vulnerabilidades en librerías (SCA)...'
                    
                    // Creamos carpeta para el reporte
                    sh "mkdir -p dependency-check-report"
                    sh "chmod 777 dependency-check-report"

                    // Ejecutamos el análisis usando Docker
                    // Esto analizará tu archivo requirements.txt
                    sh """
                        docker run --rm \
                        -u 0 \
                        -v ${WORKSPACE}:/src \
                        -v ${WORKSPACE}/dependency-check-report:/report \
                        owasp/dependency-check \
                        --scan /src \
                        --format "HTML" \
                        --project "Vulnerable App" \
                        --out /report || true
                    """
                }
            }
        }
    }

    post {
        always {
            echo '📄 Archivando todos los reportes...'
            // Reporte de ZAP
            archiveArtifacts artifacts: 'zap_reports/zap_report.html', allowEmptyArchive: true
            // Reporte de Dependencias
            archiveArtifacts artifacts: 'dependency-check-report/dependency-check-report.html', allowEmptyArchive: true
        }
    }
}