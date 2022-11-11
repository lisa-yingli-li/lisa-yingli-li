FROM python:3.7

WORKDIR /app

ADD ./Martech_API_Automation/requirements.txt ./requirements.txt
ADD ./Martech_API_Automation Martech_API_Automation
RUN pip3 install -r requirements.txt
#RUN pip3 install ptest
#RUN apt-get update -y
#RUN apt-get install -y freetds-dev gcc curl vim

CMD ["/usr/local/bin/ptest3","-t", "Martech_API_Automation.test.ads_billing.BillingServiceTest.BillingServiceTest"]
