# ELK Stack for Log Management with NLP Integration and Automated Reporting

## Architecture Diagram
*(attached)*

---

### Tasks

#### **1. Set Up ELK Stack for Log Management**

##### **Pre-Requisites**

###### Installing Java:
```bash
sudo apt install apt-transport-https
sudo apt install openjdk-11-jdk
java -version

# Export the JAVA_HOME environment variable:
JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
```

###### Creating Dedicated Users for ELK Services:
```bash
sudo adduser elasticsearch
sudo adduser logstash
sudo adduser kibana

# Adding these users to the sudo group
sudo usermod -aG sudo elasticsearch
sudo usermod -aG sudo logstash
sudo usermod -aG sudo kibana
```

##### **Install Elasticsearch**

Add the GPG key and repository:
```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt update
```

Install Elasticsearch:
```bash
sudo apt-get install elasticsearch
```

Configure Elasticsearch:
- Edit `/etc/elasticsearch/elasticsearch.yml`
- Update `/lib/systemd/system/elasticsearch.service` to ensure the service runs as the `elasticsearch` user.

Change ownership of directories:
```bash
sudo chown -R elasticsearch:elasticsearch /etc/elasticsearch
sudo chown -R elasticsearch:elasticsearch /var/lib/elasticsearch
```

Start the Elasticsearch service:
```bash
sudo systemctl start elasticsearch
sudo systemctl enable elasticsearch
sudo systemctl status elasticsearch
```

Verify Elasticsearch:
```bash
curl -X GET "localhost:9200"
```

##### **Install Logstash**
```bash
sudo apt-get install logstash
sudo chown -R logstash:logstash /etc/logstash
sudo chown -R logstash:logstash /var/lib/logstash
```

Edit `/etc/systemd/system/logstash.service` to ensure it runs as the `logstash` user.

Configure Logstash to read the configuration file:
```bash
grep path.config /etc/logstash/logstash.yml
# Set the path if not already configured
vi /etc/logstash/logstash.yml
```

Start the Logstash service:
```bash
sudo systemctl daemon-reload
sudo systemctl start logstash
sudo systemctl enable logstash
sudo systemctl status logstash
```
- Extend NLP processing with additional compliance rules.