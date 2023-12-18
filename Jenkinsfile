pipeline {
    agent any
    
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage("Pull SCM"){
            steps{
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'githubPass', url: 'https://github.com/tejasdevgekar/kronex']])
                script {
                    def scmVars = checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[credentialsId: 'githubPass', url: 'https://github.com/tejasdevgekar/kronex']]])
                    env.GIT_COMMIT = scmVars.GIT_COMMIT
                    env.SHORT_COMMIT = "${GIT_COMMIT[0..6]}"
                }
            }
        }
        stage("Build dockerfile"){
            steps {
                //sh 'export sha=`echo $GIT_COMMIT | cut -c1-7` && docker push tejasdevgekar/test2:$sha'
                script { 
                    docker.withRegistry('', 'dockerhub-kronex') {
                        def customImage = docker.build("tejasdevgekar/knorexapi:${env.SHORT_COMMIT}")
                        customImage.push()
                    }
                }
            }
        }
        stage("Gcloud auth") {
            steps {
                withCredentials([file(credentialsId: 'GKE-bruin-SA', variable: 'GC_KEY')]) {
                    sh("gcloud auth activate-service-account --key-file=${GC_KEY}")
                }
                withCredentials([string(credentialsId: 'GKE-project-id', variable: 'project')]){
                    sh("gcloud container clusters get-credentials cluster-1 --zone us-central1-c --project ${project}")
                }
            }
        }
        stage("push manifests") { 
            steps {
                //since no image with latest tag pushed, replaced latest with current sha
                sh "sed -i s/:latest/:${env.SHORT_COMMIT}/ ./manifests/knx-key-value-assignment.yml"
                sh 'kubectl apply -f ./manifests/knx-key-value-assignment.yml'
            }
        }
    }
}