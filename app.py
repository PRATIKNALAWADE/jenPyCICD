from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Jenkins server details
jenkins_url = 'http://jenkins-server.com'
job_name = 'your-job-name'
username = 'your-username'
api_token = 'your-api-token'

@app.route('/webhook', methods=['POST'])
def github_webhook():
    payload = request.json

    # Extract branch name and commit ID from the payload
    branch_name = payload['ref'].split('/')[-1]  # Get the branch name
    commit_id = payload['after']

    # Only trigger the job if it's the main branch
    if branch_name == 'main':
        job_url = f'{jenkins_url}/job/{job_name}/buildWithParameters'
        params = {
            'BRANCH_NAME': branch_name,
            'COMMIT_ID': commit_id
        }

        response = requests.post(job_url, auth=(username, api_token), params=params)

        if response.status_code == 201:
            return jsonify({'message': 'Jenkins job triggered successfully.'}), 201
        else:
            return jsonify({'message': 'Failed to trigger Jenkins job.'}), response.status_code

    return jsonify({'message': 'No action taken.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
