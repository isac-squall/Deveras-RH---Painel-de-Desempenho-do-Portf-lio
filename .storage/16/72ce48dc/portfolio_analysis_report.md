# Portfolio Analysis Report - Deveras RH

## Data Overview
- Total contracts analyzed: 5,497
- Contracts with valid financial data: 3,888 (70.7%)
- Operating units: ALPHAVILLE, BH, OSASCO, BRASILIA, DOMICILIAR, SAO JOSE DOS CAMPOS, MORUMBI, LINS, PAULINIA, CAMPINAS
- Total portfolio value: R$ 165,567,533.31

## Key Portfolio Metrics by Operating Unit

### ALPHAVILLE
- Contracts: 1,652
- Contracts with valid financial data: 1,631 (98.7%)
- Total value: R$ 77,569,468.39
- Average value per contract: R$ 47,559.45
- Value range: R$ 3,000.00 to R$ 124,526.12
- Average sessions: 14.9
- Primary status: ATIVO (43.0% of contracts)
- Primary operator: BRADESCO (42.1% of contracts)

### BH
- Contracts: 807
- Contracts with valid financial data: 757 (93.8%)
- Total value: R$ 21,331,388.35
- Average value per contract: R$ 28,178.85
- Value range: R$ 8.00 to R$ 84,354.34
- Average sessions: 12.6
- Primary status: ATIVO (43.1% of contracts)
- Primary operator: BRADESCO REEMBOLSO (39.4% of contracts)

### OSASCO
- Contracts: 5
- Contracts with valid financial data: 4 (80.0%)
- Total value: R$ 15,450.00
- Average value per contract: R$ 3,862.50
- Value range: R$ 3,075.00 to R$ 6,200.00
- Average sessions: 12.2
- Primary status: ATIVO (60.0% of contracts)
- Primary operator: AMIL (100.0% of contracts)

### BRASILIA
- Contracts: 1
- Contracts with valid financial data: 0 (0.0%)
- Total value: R$ 0.00
- Average value per contract: R$ nan
- Value range: R$ nan to R$ nan
- Average sessions: 13.0
- Primary status: ATIVO (100.0% of contracts)
- Primary operator: AMIL (100.0% of contracts)

### DOMICILIAR
- Contracts: 1,622
- Contracts with valid financial data: 386 (23.8%)
- Total value: R$ 16,678,035.16
- Average value per contract: R$ 43,207.34
- Value range: R$ 2,600.00 to R$ 103,540.33
- Average sessions: 16.3
- Primary status: ATIVO (43.2% of contracts)
- Primary operator: BRADESCO (38.8% of contracts)

### SAO JOSE DOS CAMPOS
- Contracts: 841
- Contracts with valid financial data: 731 (86.9%)
- Total value: R$ 32,521,622.85
- Average value per contract: R$ 44,489.22
- Value range: R$ 2,600.00 to R$ 158,214.06
- Average sessions: 16.3
- Primary status: ATIVO (44.0% of contracts)
- Primary operator: SULAMERICA  (42.7% of contracts)

### MORUMBI
- Contracts: 59
- Contracts with valid financial data: 0 (0.0%)
- Total value: R$ 0.00
- Average value per contract: R$ nan
- Value range: R$ nan to R$ nan
- Average sessions: 16.0
- Primary status: ATIVO (44.1% of contracts)
- Primary operator: SULAMERICA  (59.3% of contracts)

### LINS
- Contracts: 65
- Contracts with valid financial data: 12 (18.5%)
- Total value: R$ 488,200.57
- Average value per contract: R$ 40,683.38
- Value range: R$ 8,800.00 to R$ 59,193.82
- Average sessions: 16.5
- Primary status: ATIVO (40.0% of contracts)
- Primary operator: SULAMERICA  (87.7% of contracts)

### PAULINIA
- Contracts: 251
- Contracts with valid financial data: 218 (86.9%)
- Total value: R$ 11,587,072.35
- Average value per contract: R$ 53,151.71
- Value range: R$ 6,167.61 to R$ 101,950.24
- Average sessions: 16.3
- Primary status: ATIVO (44.2% of contracts)
- Primary operator: VIVEST (33.5% of contracts)

### CAMPINAS
- Contracts: 194
- Contracts with valid financial data: 149 (76.8%)
- Total value: R$ 5,376,295.64
- Average value per contract: R$ 36,082.52
- Value range: R$ 3,681.72 to R$ 89,595.06
- Average sessions: 16.3
- Primary status: ATIVO (44.3% of contracts)
- Primary operator: SULAMERICA (36.1% of contracts)

## Data Inconsistencies Identified

1. **Inconsistent Column Naming**: Different sheets used varied naming conventions for the same data.
2. **Inconsistent Location Names**: The same operating unit appeared under different names (e.g., 'ALPHAVILLE', 'alpha').
3. **Client ID Inconsistencies**: Multiple patient names were assigned to the same client ID.
4. **Data Type Inconsistencies**: The same columns had different data types across sheets.
5. **Problematic Date Values**: Some sheets contained unusual date values (dates before 2000).
6. **Extreme Values in VALOR Column**: SJC and PAULINIA sheets contained datetime values incorrectly interpreted as currency.
7. **Missing Values**: Critical columns contained significant numbers of missing values.

## Recommendations for Dashboard Creation

1. Use the standardized processed data provided in the CSV file for consistent analysis.
2. Implement filters by operating unit, status, and insurance operator.
3. Include time series visualizations to track portfolio growth over time.
4. Create separate panels for individual operating unit performance and consolidated views.
5. Consider implementing alerts for contracts with unusual values or statuses.
6. Include data quality metrics to monitor completeness and consistency.
