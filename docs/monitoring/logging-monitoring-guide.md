# Logging and Monitoring in Azure Synapse Analytics

This guide provides comprehensive information on setting up logging, monitoring, and alerting for Azure Synapse Analytics workspaces and their components, helping you maintain operational visibility and quickly respond to issues.

## Introduction to Synapse Monitoring

Azure Synapse Analytics provides multiple layers of monitoring capabilities to give you deep insights into your data platform's performance, availability, and health. Effective monitoring helps you:

- Detect and diagnose issues before they impact users
- Track resource utilization and optimize costs
- Monitor performance across all Synapse components
- Create alerts for critical conditions
- Maintain audit trails for security and compliance

## Monitoring Architecture

A comprehensive monitoring solution for Azure Synapse Analytics typically involves:

1. **Azure Monitor**: The foundational monitoring service for all Azure resources
2. **Log Analytics**: Collection, aggregation, and analysis of telemetry and log data
3. **Azure Metrics**: Near real-time performance and health metrics
4. **Application Insights**: Deep application monitoring for custom applications
5. **Diagnostic Settings**: Configuration of log and metric collection
6. **Alerting**: Proactive notification when issues arise

![Synapse Monitoring Architecture](../images/monitoring-architecture.png)

## Setting Up Diagnostic Logging

### Configuring Diagnostic Settings

To enable comprehensive logging for your Synapse workspace:

1. Navigate to your Synapse workspace in the Azure portal
2. Select **Diagnostic settings** under Monitoring
3. Click **Add diagnostic setting**
4. Provide a name for your settings
5. Select the logs and metrics you want to collect
6. Choose destination(s) for your logs:
   - Log Analytics workspace
   - Storage account
   - Event Hub

```powershell
# PowerShell: Configure diagnostic settings for Synapse workspace
$workspace = Get-AzSynapseWorkspace -Name "mysynapseworkspace" -ResourceGroupName "myresourcegroup"
$logAnalytics = Get-AzOperationalInsightsWorkspace -ResourceGroupName "myresourcegroup" -Name "mylogworkspace"

Set-AzDiagnosticSetting -ResourceId $workspace.Id `
                        -Name "SynapseDiagnostics" `
                        -WorkspaceId $logAnalytics.ResourceId `
                        -Category @("SynapseRbacOperations", "SQLSecurityAuditEvents", "SynapseLinkEvent", "IntegrationPipelineRuns", "IntegrationActivityRuns", "IntegrationTriggerRuns", "SynapseSqlPoolExecRequests", "SynapseSqlPoolRequestSteps", "SynapseSqlPoolDmsWorkers", "SynapseBuiltinSqlPoolRequestsEnded") `
                        -MetricCategory @("AllMetrics") `
                        -EnableLog $true `
                        -EnableMetrics $true
```

### Key Log Categories to Enable

| Component | Log Categories | Information Provided |
|-----------|---------------|---------------------|
| Workspace | SynapseRbacOperations | Role-based access control operations |
| SQL | SQLSecurityAuditEvents | SQL security audit events |
| SQL | SynapseSqlPoolExecRequests | SQL pool execution requests |
| SQL | SynapseSqlPoolRequestSteps | SQL pool request steps |
| SQL | SynapseSqlPoolDmsWorkers | SQL pool DMS worker operations |
| SQL Serverless | SynapseBuiltinSqlPoolRequestsEnded | Serverless SQL pool request information |
| Spark | SparkJobEvents | Spark job lifecycle events |
| Spark | SparkStageEvents | Spark stage execution information |
| Pipeline | IntegrationPipelineRuns | Pipeline run information |
| Pipeline | IntegrationActivityRuns | Activity run information |
| Pipeline | IntegrationTriggerRuns | Trigger execution information |

### Storage Options for Logs

Each storage option has specific benefits:

1. **Log Analytics Workspace**:
   - Best for interactive querying and analysis
   - Supports complex KQL queries and dashboards
   - Enables cross-component correlation
   - Powers alerting based on log queries

2. **Azure Storage Account**:
   - Long-term retention of logs
   - Cost-effective for large volumes
   - Useful for compliance and audit requirements
   - Can be analyzed using other tools like Power BI

3. **Event Hub**:
   - Real-time log streaming to external systems
   - Integration with third-party SIEM solutions
   - Custom real-time processing pipelines
   - Useful for cross-cloud monitoring scenarios

## Key Metrics to Monitor

### SQL Pool Metrics

| Metric | Description | Threshold Guidance |
|--------|-------------|-------------------|
| DWU/cDWU Percentage | Percentage of compute resources used | >80% sustained indicates potential need for scaling |
| CPU Percentage | CPU utilization | >90% indicates compute pressure |
| Data IO Percentage | Data IO utilization | >80% indicates IO bottleneck |
| Active Queries | Number of queries running | Monitor for unexpected spikes |
| Queued Queries | Number of queries waiting | >0 indicates resource constraints |
| Successful Connections | Connection success rate | <95% indicates connection issues |
| Failed Connections | Connection failures | Any failures warrant investigation |
| Storage Size | Data storage consumed | Track growth trends for capacity planning |

### Spark Pool Metrics

| Metric | Description | Threshold Guidance |
|--------|-------------|-------------------|
| Active Applications | Number of running Spark apps | Compare against available resources |
| Pending Applications | Apps waiting for resources | >0 indicates resource constraints |
| Cores In Use | Number of CPU cores in use | >80% of provisioned cores indicates scaling need |
| Memory In Use | Amount of memory used | >80% indicates potential memory pressure |
| Application Failure Rate | Percentage of failed applications | >5% warrants investigation |
| Job Completion Time | Time taken to complete jobs | Monitor for trends/degradation |

### Pipeline Metrics

| Metric | Description | Threshold Guidance |
|--------|-------------|-------------------|
| Pipeline Success Rate | Percentage of successful runs | <95% warrants investigation |
| Pipeline Run Time | Duration of pipeline execution | Monitor for trends/degradation |
| Activity Success Rate | Success rate of individual activities | <95% for critical activities needs attention |
| Integration Runtime CPU | CPU utilization of integration runtime | >80% indicates scaling need |
| Integration Runtime Memory | Memory utilization | >80% indicates scaling need |
| Queued Pipeline Runs | Number of pipelines waiting to run | >0 indicates resource constraints |

## Creating a Monitoring Dashboard

Azure provides built-in dashboards, but you can create custom dashboards for Synapse monitoring:

1. Navigate to **Dashboard** in the Azure portal
2. Click **+ New dashboard**
3. Name your dashboard (e.g., "Synapse Monitoring")
4. Add tiles using the gallery or pin metrics from your resources
5. Organize tiles in logical groups:
   - Health and availability
   - Performance metrics
   - Resource utilization
   - Recent failures
   - Cost insights

### Key Sections for Your Dashboard

1. **Workspace Health**:
   - Overall workspace status
   - Recent operations

2. **SQL Pool Performance**:
   - DWU/cDWU utilization
   - Active vs. queued queries
   - Data IO and tempdb usage

3. **Spark Performance**:
   - Active applications
   - Core and memory utilization
   - Job success rates

4. **Pipeline Execution**:
   - Success/failure rates
   - Pipeline duration trends
   - Activity performance

5. **Security and Access**:
   - Failed login attempts
   - RBAC operations
   - Firewall blocks

## Setting Up Alerts

### Critical Alerts to Configure

1. **Health and Availability**:
   - Workspace availability drops below 100%
   - Service health incidents affecting Synapse
   - Failed connectivity to dependent services

2. **Performance Alerts**:
   - SQL Pool: DWU utilization >90% for >30 minutes
   - SQL Pool: Queued queries >5 for >10 minutes
   - Spark Pool: Pending applications >3 for >15 minutes
   - Pipeline: Run duration >150% of baseline
   - Integration Runtime: CPU >90% for >15 minutes

3. **Failure Alerts**:
   - SQL: Failed queries >5 in 10 minutes
   - Spark: Failed jobs >3 in 1 hour
   - Pipelines: Success rate <90% in last hour
   - Authentication: Failed logins >10 in 5 minutes

### Alert Configuration

```powershell
# PowerShell: Create alert for high DWU utilization
$scope = "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Synapse/workspaces/{workspace-name}/sqlPools/{sql-pool-name}"
$criteriaObject = New-AzMetricAlertRuleV2Criteria -MetricName "DWUUsagePercent" -TimeAggregation "Average" -Operator "GreaterThan" -Threshold 90

Add-AzMetricAlertRuleV2 -Name "High DWU Alert" `
                        -ResourceGroupName "myresourcegroup" `
                        -WindowSize 00:30:00 `
                        -Frequency 00:05:00 `
                        -TargetResourceId $scope `
                        -Condition $criteriaObject `
                        -ActionGroup "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/microsoft.insights/actionGroups/{action-group-name}" `
                        -Severity 2
```

### Action Groups for Alert Notifications

Create action groups to define what happens when alerts are triggered:

1. Navigate to **Monitor > Alerts > Action Groups**
2. Click **+ Add action group**
3. Configure notification methods:
   - Email: For non-urgent notifications
   - SMS: For critical alerts requiring immediate attention
   - Voice call: For highest severity alerts
   - Azure Functions: For automated remediation
   - Logic Apps: For complex alert handling workflows
   - Webhook: For integration with external systems

## Monitoring with Log Analytics

### Key KQL Queries for Synapse

#### SQL Pool Performance Issues

```kusto
// Long-running queries
SynapseSqlPoolExecRequests
| where TimeGenerated > ago(24h)
| where Status == "Running"
| extend duration_minutes = datetime_diff('minute', now(), StartTime)
| where duration_minutes > 60  // Queries running longer than 60 minutes
| project QueryText, LoginName, Label, ResourceClass, duration_minutes, StartTime
| order by duration_minutes desc

// Blocked queries
SynapseSqlPoolExecRequests
| where TimeGenerated > ago(24h)
| where IsBlocked == 1
| project RequestId, QueryText, LoginName, BlockedBy, Status, StartTime, EndCompileTime
| order by StartTime desc

// Query errors
SynapseSqlPoolExecRequests
| where TimeGenerated > ago(24h)
| where Status == "Failed"
| project QueryText, ErrorMessage, LoginName, StartTime
| order by StartTime desc
```

#### Spark Job Monitoring

```kusto
// Failed Spark jobs
SparkJobEvents
| where TimeGenerated > ago(24h)
| where Result == "Failed"
| project JobId, JobName, SubmissionTime, StartTime, EndTime, StageIds
| join kind=inner (
    SparkStageEvents
    | where Result == "Failed"
    | project StageId, StageAttemptId, SubmissionTime, CompletionTime, FailureReason
) on $left.StageIds == $right.StageId
| project JobId, JobName, StageId, StartTime, CompletionTime, FailureReason
| order by StartTime desc

// Long-running Spark jobs
SparkJobEvents
| where TimeGenerated > ago(24h)
| where Result == "Succeeded"
| extend duration_minutes = datetime_diff('minute', EndTime, StartTime)
| where duration_minutes > 30  // Jobs running longer than 30 minutes
| project JobId, JobName, StartTime, EndTime, duration_minutes
| order by duration_minutes desc
```

#### Pipeline Execution Analysis

```kusto
// Failed pipeline runs
SynapseIntegrationPipelineRuns
| where TimeGenerated > ago(24h)
| where Status == "Failed"
| project TimeGenerated, PipelineName, RunId, Parameters, FailureType, ErrorMessage
| order by TimeGenerated desc

// Pipeline performance trends
SynapseIntegrationPipelineRuns
| where TimeGenerated > ago(7d)
| where Status == "Succeeded"
| extend DurationInMinutes = todouble(DurationInMs)/1000/60
| summarize AvgDuration = avg(DurationInMinutes), MaxDuration = max(DurationInMinutes), RunCount = count() by PipelineName, bin(TimeGenerated, 1d)
| order by TimeGenerated asc
```

### Workbooks for Synapse Monitoring

Azure Workbooks provide interactive reports for monitoring. Create workbooks for:

1. **SQL Pool Performance Dashboard**:
   - Query performance trends
   - Resource utilization patterns
   - Top resource-intensive queries
   - Concurrency metrics

2. **Spark Job Analysis**:
   - Job success/failure rates
   - Execution time trends
   - Resource consumption patterns
   - Application logs

3. **Pipeline Execution Monitoring**:
   - Pipeline health overview
   - Duration trends by pipeline
   - Activity failure analysis
   - Trigger reliability metrics

### Sample Workbook Structure

```json
{
  "version": "Notebook/1.0",
  "items": [
    {
      "type": 1,
      "content": {
        "json": "# Synapse SQL Pool Performance"
      }
    },
    {
      "type": 9,
      "content": {
        "version": "KqlParameterItem/1.0",
        "parameters": [
          {
            "id": "f503a201-9a03-4926-8a3f-882ba6224781",
            "version": "KqlParameterItem/1.0",
            "name": "TimeRange",
            "type": 4,
            "value": { "durationMs": 86400000 },
            "typeSettings": { "selectableValues": [ {"durationMs": 3600000}, {"durationMs": 86400000}, {"durationMs": 604800000} ] }
          }
        ]
      }
    },
    {
      "type": 3,
      "content": {
        "version": "KqlItem/1.0",
        "query": "SynapseSqlPoolExecRequests | where TimeGenerated > ago({TimeRange}) | summarize count() by bin(TimeGenerated, 1h), Status",
        "size": 0,
        "title": "Query Status Over Time",
        "timeContext": { "durationMs": 86400000 },
        "queryType": 0,
        "resourceType": "microsoft.operationalinsights/workspaces",
        "visualization": "areachart"
      }
    }
  ]
}
```

## Implementing Azure Monitor for Synapse

### Holistic Monitoring Approach

Implement a comprehensive monitoring strategy:

1. **Real-time operational monitoring**:
   - Dashboards for current state visibility
   - Alerts for immediate response
   - Resource health monitoring

2. **Performance analysis**:
   - Trend analysis across components
   - Query store for SQL performance
   - Spark history server integration

3. **Cost and resource optimization**:
   - DWU/Spark core utilization
   - Idle resource detection
   - Scaling opportunity identification

4. **Security and compliance monitoring**:
   - Authentication failures
   - Firewall events
   - RBAC changes
   - Data access patterns

### Security Monitoring with Microsoft Sentinel

For advanced security monitoring:

1. Connect your Log Analytics workspace to Microsoft Sentinel
2. Enable the Azure Synapse Analytics data connector
3. Implement built-in analytics rules for Synapse
4. Create custom detection rules for your environment
5. Set up security incident response playbooks

## Advanced Monitoring Scenarios

### Integrating with DevOps Processes

1. **Deployment Monitoring**:
   - Track performance before/after deployments
   - Set up alerts for post-deployment issues
   - Integrate monitoring data into CI/CD pipelines

2. **Infrastructure as Code**:
   - Automate creation of monitoring resources
   - Version control dashboard and alert configurations
   - Script diagnostic setting deployment

```yaml
# Azure Pipeline YAML for deploying monitoring resources
steps:
- task: AzurePowerShell@5
  inputs:
    azureSubscription: 'MyAzureSubscription'
    ScriptType: 'FilePath'
    ScriptPath: 'deploy-monitoring.ps1'
    azurePowerShellVersion: 'LatestVersion'
```

### End-to-End Pipeline Monitoring

For complex data pipelines spanning multiple services:

1. Create a unified monitoring solution across:
   - Azure Data Factory/Synapse Pipelines
   - Data sources and sinks
   - Downstream consumers (Power BI, applications)

2. Implement correlation IDs for end-to-end tracing
3. Set up business metrics to track data quality and processing SLAs

### Hybrid Monitoring Solutions

For environments with on-premises components:

1. Use Azure Arc for consistent monitoring across environments
2. Implement Azure Monitor agents for on-premises servers
3. Create unified dashboards spanning cloud and on-premises

## Best Practices

### Monitoring Strategy

- Start with core metrics and expand gradually
- Balance comprehensive monitoring with cost optimization
- Review and refine alert thresholds regularly
- Document monitoring setup as part of operational procedures

### Performance Optimization

- Use monitoring data to right-size resources
- Establish performance baselines for all components
- Track trends to identify gradual degradation
- Correlate metrics across components for root cause analysis

### Operational Excellence

- Assign clear ownership for monitoring and alerts
- Document response procedures for common alerts
- Conduct regular reviews of monitoring effectiveness
- Continuously refine monitoring based on incidents and outages

## Related Topics

- [Troubleshooting with Logs](../troubleshooting/index.md)
- [Performance Optimization](../best-practices/performance.md)
- [Security Monitoring](../best-practices/security.md#monitoring)
- [Cost Management](../best-practices/cost-optimization.md)

## External Resources

- [Azure Monitor Documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/)
- [Kusto Query Language Reference](https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/)
- [Azure Workbooks Documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-overview)
- [Microsoft Sentinel Documentation](https://docs.microsoft.com/en-us/azure/sentinel/)
