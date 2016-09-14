node('dockerhub') {
  def repo = "cloudbees/jenkins-enterprise"
  def branch = "cje"

  stage 'Build'
  git url: 'https://github.com/cloudbees/docker.git', branch: branch
  sh "docker build --pull --no-cache --build-arg JENKINS_VERSION=${JENKINS_VERSION} --build-arg JENKINS_SHA=${JENKINS_SHA} -t ${repo}:${JENKINS_VERSION} ."
  // need --build-arg support
  //def img = docker.build("${repo}:${JENKINS_VERSION}")
  def img = docker.image("${repo}:${JENKINS_VERSION}")
  img.tag("latest")

  stage 'Push'
  docker.withRegistry('', 'dockerhub') {
    img.push();
    img.push('latest');
  }
}
