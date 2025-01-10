# ELK Stack for Log Management with NLP Integration and Automated Reporting
## Learn More
For a detailed explanation of this project, check out my [LinkedIn article](https://www.linkedin.com/pulse/nlp-driven-automated-compliance-reporting-elk-stack-hamza-afzal-bi0me).


## Architecture Diagram
*(See reference in image files attached)*

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
##### **Install Kibana**
```bash
sudo apt-get install kibana
sudo chown -R kibana:kibana /etc/kibana
sudo chown -R kibana:kibana /var/lib/kibana
```

Configure Kibana:
- Edit `/etc/kibana/kibana.yml`

Start the Kibana service:
```bash
sudo systemctl daemon-reload
sudo systemctl start kibana
sudo systemctl enable kibana
sudo systemctl status kibana
```

Access Kibana at: `http://<ip_address>:5601`

---

#### **2. Parsing System Logs**

Grant `logstash` user read access to `/var/log/syslog`:
```bash
usermod -a -G adm logstash
```
Create a Logstash configuration file `/etc/logstash/conf.d/syslog.conf`:
```plaintext
input {
  file {
    path => "/var/log/syslog"
    start_position => "beginning"
    sincedb_path => "/dev/null"
  }
}

filter {
  grok {
    match => { "message" => "%{SYSLOGTIMESTAMP:syslog_timestamp} %{HOSTNAME:hostname} %{SYSLOGPROG:program}: %{GREEDYDATA:log_message}" }
  }
  date {
    match => [ "syslog_timestamp", "MMM d HH:mm:ss" ]
    timezone => "Etc/UTC"
    target => "@timestamp"
  }
}

output {
  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "syslog-%{+YYYY.MM.dd}"
  }
}
```

Restart Logstash:
```bash
sudo systemctl restart logstash
```

---

#### **3. Integrating NLP with Logstash**

##### Generate Sample Logs:
```bash
# GDPR-related logs
echo "User 12345 accessed sensitive data: PII (Personally Identifiable Information)" >> /var/log/syslog
```

##### Python NLP Script:
Create `/usr/local/logstash_scripts/nlp_processor.py`:
```python
#!/usr/bin/env python3
# Add your Python code here
# see nlp-processor.py file attached
```

##### Configure Logstash Pipeline:
Edit `/etc/logstash/conf.d/compliance.conf`.
```python
# see the compliance.conf file attached
```
Restart Logstash:
```bash
sudo systemctl restart logstash
```

---

#### **4. Automating Reporting**

Create `/usr/local/logstash_scripts/compliance_report.py`:
```python
#!/usr/bin/env python3
# Add your Python code here
# see the compliance_report.py attached
```

Run the script:
```bash
/var/lib/logstash/venv/bin/python3 /usr/local/logstash_scripts/compliance_report.py
```

---

### Future Enhancements

- Use a cron job to automate reporting.
- Extend NLP processing with additional compliance rules.