DROP VIEW IF EXISTS vw_campaign_roi_map;
CREATE VIEW vw_campaign_roi_map AS
SELECT
  channel,
  SUM(spend) AS spend,
  AVG(roi) AS roi_avg,
  COUNT(*) AS n_rows
FROM campaign_performance
GROUP BY channel;
