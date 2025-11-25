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
                    
                    // debug=False es vital para que funcionen las métricas
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
                    
                    sh "rm -rf zap_reports"
                    sh "mkdir -p zap_reports"
                    sh "docker rm -f zap-scanner || true"

                    echo '🔥 Ejecutando ZAP Scan...'
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
                    
                    // 1. Limpieza y preparación
                    sh "rm -rf dependency-check-report"
                    sh "mkdir -p dependency-check-report"
                    sh "docker rm -f odc-scanner || true"

                    // 2. Ejecutar escáner SIN montar volumen de salida, solo nombre fijo
                    // Nota: Mantenemos el volumen de entrada (-v ${WORKSPACE}:/src) para que lea el requirements.txt
                    sh """
                        docker run \
                        --name odc-scanner \
                        -u 0 \
                        -v ${WORKSPACE}:/src \
                        owasp/dependency-check \
                        --scan /src \
                        --format "HTML" \
                        --project "Vulnerable App" \
                        --out /report \
                        --disableRetireJS \
                        --disableNodeJS \
                        --disableYarnAudit || true
                    """
                    
                    // 3. Extraer el reporte manualmente del contenedor
                    echo '📥 Extrayendo reporte de Dependencias...'
                    sh "docker cp odc-scanner:/report/dependency-check-report.html ./dependency-check-report/dependency-check-report.html"
                    
                    // 4. Borrar contenedor
                    sh "docker rm odc-scanner"
                }
            }
        }
    }

    post {
        always {
            echo '📄 Archivando todos los reportes...'
            archiveArtifacts artifacts: 'zap_reports/zap_report.html', allowEmptyArchive: true
            archiveArtifacts artifacts: 'dependency-check-report/dependency-check-report.html', allowEmptyArchive: true
        }
    }
}