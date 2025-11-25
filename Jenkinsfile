pipeline {
    agent any

    stages {
        stage('Diagnóstico ZAP') {
            steps {
                script {
                    echo '🔍 Iniciando diagnóstico de rutas en el contenedor ZAP...'
                    
                    // 1. Listar el contenido de la carpeta /zap para ver qué hay
                    echo '📂 Listando contenido de /zap:'
                    sh "docker run --rm -t zaproxy/zap-stable ls -la /zap/"
                    
                    // 2. Buscar dónde está el archivo exacto en todo el sistema de archivos
                    echo '🔎 Buscando zap-baseline-scan.py en todo el contenedor:'
                    sh "docker run --rm -t zaproxy/zap-stable find / -name zap-baseline-scan.py"
                    
                    // 3. Ver las variables de entorno (PATH)
                    echo '🌐 Verificando variables de entorno:'
                    sh "docker run --rm -t zaproxy/zap-stable env"
                }
            }
        }
    }
}