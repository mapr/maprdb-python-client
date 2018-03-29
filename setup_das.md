##Steps for start the data access service.
####Internal use only

**Update or install maven 3.5.x++:**
  * `sudo yum remove maven`
  * `sudo wget http://apache.cp.if.ua/maven/maven-3/3.5.2/binaries/apache-maven-3.5.2-bin.tar.gz`
  * `tar -xzvf apache-maven-3.5.2-bin.tar.gz`
  * `mv apache-maven-3.5.2 maven`
  * Create maven.sh file `sudo vi /etc/profile.d/maven.sh`
  * Insert into maven.sh
      ```
          export M2_HOME=/home/mapr/maven
          export PATH=${M2_HOME}/bin:${PATH}
      ```
  * Execute `source /etc/profile.d/maven.sh`
  
**Install service.**
1) Clone data access service repo from github:
 `git clone https://github.com/mapr/maprdb-grpc-service.git` and 
 `cd maprdb-grpc-service`
2) Update root pom.xml file (**in case if you not in US office**)
    ```<repositories>
            <repository>
                <id>mapr-artifactory</id>
                <url>http://artifactory.devops.lab/artifactory/maven-mapr-central/</url>
                <snapshots><enabled>true</enabled></snapshots>
                <releases><enabled>true</enabled></releases>
            </repository>
            <repository>
                <id>mapr-releases</id>
                <url>http://repository.mapr.com/maven/</url>
                <snapshots><enabled>false</enabled></snapshots>
                <releases><enabled>true</enabled></releases>
            </repository>
            <repository>
                <id>repository_cv</id>
                <name>Private MapR repo for CyberVision</name>
                <url>http://23.21.204.176/nexus/content/groups/mapr-public/</url>
                <releases>
                    <enabled>true</enabled>
                </releases>
                <snapshots>
                    <enabled>true</enabled>
                </snapshots>
            </repository>
        </repositories>
3) Build and launch service:
 * `mvn clean install -DskipTests`
 * `cd launcher/`
 * `mvn exec:java -Dexec.mainClass="com.mapr.data.service.Launcher"`
 

After steps above you should see in you terminal that service listening port 5678.
