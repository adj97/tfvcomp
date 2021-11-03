# tfvars_compare

Generic python code to compare terraform variables files (.tfvars.json) and output to a csv file in a table

## How to run this tool

Pull the repository to your local machine

Add the following to your bash alias
```bash
tfvcomp(){
        python3 /...codepath.../main.py $@
}
```

go to your terraform directory
`cd ~/...terraform_repo_path.../vars`

execute tfvcomp to compare files test1.tfvars.json and test2.tfvars.json like so (without file extensions)
`tfvcomp test1 test2 ...`
