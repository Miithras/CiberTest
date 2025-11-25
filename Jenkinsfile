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
        stage('Limpieza y Checkout') {
            steps {
                script {
                    echo '🧹 Limpiando espacio de trabajo...'
                    cleanWs() // Borra todo lo viejo
                    
                    echo '📥 Descargando código actualizado desde GitHub...'
                    checkout scm // Fuerza la descarga de la última versión
                    
                    echo '👀 VERIFICACIÓN DE VERSIONES (LO QUE JENKINS VE):'
                    // Esto imprimirá en la consola el contenido exacto del archivo
                    sh "cat requirements.txt" 
                }
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
                    
                    // debug=False es vital para métricas
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
                    echo '⏳ Esperando 10 segundos...'
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
                    
                    sh "docker cp zap-scanner:/zap/wrk/zap_report.html ./zap_reports/zap_report.html"
                    sh "docker rm zap-scanner"
                }
            }
        }

        stage('Análisis de Dependencias (Dependency Check)') {
            steps {
                script {
                    echo '🔍 Analizando vulnerabilidades (SCA)...'
                    
                    sh "rm -rf dependency-check-report"
                    sh "mkdir -p dependency-check-report"
                    sh "docker rm -f odc-scanner || true"

                    // Iniciar contenedor
                    sh "docker run -d -u 0 --name odc-scanner --entrypoint tail owasp/dependency-check -f /dev/null"

                    // Crear carpeta interna
                    sh "docker exec odc-scanner mkdir -p /src"

                    // Copiar requirements.txt
                    sh "docker cp ${WORKSPACE}/requirements.txt odc-scanner:/src/requirements.txt"
                    
                    // Ejecutar escaneo con Flags Experimentales y desactivando JS
                    withCredentials([string(credentialsId: 'nvd-api-key', variable: 'NVD_KEY')]) {
                        sh """
                            docker exec odc-scanner /usr/share/dependency-check/bin/dependency-check.sh \
                            --scan /src \
                            --format "HTML" \
                            --project "Vulnerable App" \
                            --out /report \
                            --nvdApiKey ${NVD_KEY} \
                            --disableRetireJS \
                            --disableNodeJS \
                            --disableYarnAudit \
                            --enableExperimental
                        """
                    }
                    
                    echo '📥 Extrayendo reporte...'
                    sh "docker cp odc-scanner:/report/dependency-check-report.html ./dependency-check-report/dependency-check-report.html"
                    
                    sh "docker rm -f odc-scanner"
                }
            }
        }
    }

    post {
        always {
            echo '📄 Archivando reportes...'
            archiveArtifacts artifacts: 'zap_reports/zap_report.html', allowEmptyArchive: true
            archiveArtifacts artifacts: 'dependency-check-report/dependency-check-report.html', allowEmptyArchive: true
        }
    }
}