DROP VIEW IF EXISTS vw_marketing_kpi;
CREATE VIEW vw_marketing_kpi AS
SELECT
  DATE(date) AS dt,
  SUM(spend) AS spend,
  SUM(impressions) AS impressions,
  SUM(clicks) AS clicks,
  CASE WHEN SUM(impressions)=0 THEN 0.0 ELSE SUM(clicks)*1.0/SUM(impressions) END AS ctr,
  AVG(cpc) AS cpc_avg,
  AVG(cpm) AS cpm_avg,
  AVG(roi) AS roi_avg,
  AVG(engagement_rate) AS engagement_rate_avg
FROM campaign_performance
GROUP BY DATE(date);
