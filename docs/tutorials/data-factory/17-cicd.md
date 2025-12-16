# 🚀 CI/CD Integration

> __🏠 [Home](../../../README.md)__ | __📖 [Documentation](../../README.md)__ | __🎓 [Tutorials](../README.md)__ | __🔄 [Data Factory](README.md)__ | __CI/CD__

![Tutorial](https://img.shields.io/badge/Tutorial-CI_CD_Integration-blue)
![Duration](https://img.shields.io/badge/Duration-20_minutes-green)
![Level](https://img.shields.io/badge/Level-Advanced-red)

__Implement continuous integration and deployment for Azure Data Factory using ARM templates, Azure DevOps, and automated testing.__

## 📋 Table of Contents

- [Git Integration](#git-integration)
- [ARM Template Deployment](#arm-template-deployment)
- [Azure DevOps Pipeline](#azure-devops-pipeline)
- [Next Steps](#next-steps)

## 🔄 Git Integration

### Configure Git Repository

1. Navigate to ADF Studio > __Manage__ > __Git configuration__
2. Select repository type (Azure DevOps or GitHub)
3. Configure branches:
   - Collaboration branch: `main`
   - Publish branch: `adf_publish`

### Branch Strategy

```text
Development Flow:
├── main (collaboration)
├── feature/feature-name
├── develop
└── adf_publish (ARM templates)
```

## 📦 ARM Template Deployment

### Export ARM Template

ARM templates are automatically generated in the `adf_publish` branch.

### Deploy Using PowerShell

```powershell
# Deploy ARM template
New-AzResourceGroupDeployment `
  -ResourceGroupName "rg-adf-prod" `
  -TemplateFile "./adf_publish/ARMTemplateForFactory.json" `
  -TemplateParameterFile "./adf_publish/ARMTemplateParametersForFactory.json"
```

## 🔧 Azure DevOps Pipeline

### Build Pipeline

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: CopyFiles@2
  inputs:
    SourceFolder: '$(Build.Repository.LocalPath)/adf_publish'
    Contents: '**'
    TargetFolder: '$(Build.ArtifactStagingDirectory)'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'adf-templates'
```

### Release Pipeline

```yaml
# release-pipeline.yml
stages:
- stage: Deploy_Dev
  jobs:
  - deployment: Deploy_ADF_Dev
    environment: 'Dev'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureResourceManagerTemplateDeployment@3
            inputs:
              deploymentScope: 'Resource Group'
              azureResourceManagerConnection: 'Azure-Connection'
              resourceGroupName: 'rg-adf-dev'
              location: 'East US 2'
              templateLocation: 'Linked artifact'
              csmFile: '$(Pipeline.Workspace)/adf-templates/ARMTemplateForFactory.json'
              csmParametersFile: '$(Pipeline.Workspace)/adf-templates/ARMTemplateParametersForFactory.json'
```

## 📚 Additional Resources

- [ADF CI/CD Documentation](https://docs.microsoft.com/azure/data-factory/continuous-integration-deployment)
- [DevOps Guide](../../devops/pipeline-ci-cd.md)

## 🚀 Next Steps

__→ [18. Environment Management](18-environment-mgmt.md)__

---

__Module Progress__: 17 of 18 complete

*Tutorial Version: 1.0*
*Last Updated: January 2025*
