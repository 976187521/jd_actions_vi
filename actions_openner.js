const { Octokit } = require("@octokit/rest")
const octokit = new Octokit()

async function openner(owner, repo) {
  // Get fork disabled actions
  await octokit.request('GET /repos/{owner}/{repo}/actions/workflows', {
    owner: owner,
    repo: repo
  }).then (response => {
    inactive = response.data.workflows.filter(workflow => 
      workflow.state == 'disabled_fork')
  }).catch (error => {
    console.error(error)
  })
  // Enable actions
  inactive.forEach(workflow => {
    octokit.request('PUT /repos/{owner}/{repo}/actions/workflows/{workflow_id}/enable', {
      owner: owner,
      repo: repo,
      workflow_id: workflow.id
    }).then (response => {
      console.log(response.data)
    }).catch (error => {
      console.error(error)
    })
  })
}

let argv = process.argv.slice(2)
openner(argv[0], argv[1])