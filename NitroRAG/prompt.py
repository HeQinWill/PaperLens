# Update for v1.0.6
# https://github.com/HKUDS/LightRAG/blob/main/lightrag/prompt.py

GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["Chemical_species", "Satellite_sensor", "Measurement_instrument", "Atmospheric_model", "Radiation_model", "Retrieval_parameter", "Technology_algorithm", "Result_metric", "Policy_regulation", "Research_project", "Location_region", "Temporal_period", "Spatial_resolution", "Temporal_resolution", "Author", "Publication_year"]

PROMPTS["entity_extraction"] = """-Goal-
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types:  [Chemical_species, Satellite_sensor, Measurement_instrument, Atmospheric_model, Radiation_model, Retrieval_parameter, Technology_algorithm, Result_metric, Policy_regulation, Research_project, Location_region, Temporal_period, Spatial_resolution, Temporal_resolution, Author, Publication_year]
Text:
"Title: The version 3 OMI NO<sub>2</sub> standard productAbstract: We describe the new version 3.0 NASA Ozone Monitoring Instrument (OMI) standard nitrogen dioxide (NO2 products (SPv3). The products and documentation are publicly available from the NASA Goddard Earth Sciences Data and Information Services Center. The major improvements include (1) a new spectral fitting algorithm for NO2 slant column density (SCD) retrieval and (2) higher-resolution (1 degrees latitude and 1.25 degrees longitude) a priori NO2 and temperature profiles from the Global Modeling Initiative (GMI) chemistry-transport model with yearly varying emissions to calculate air mass factors (AMFs) required to convert SCDs into vertical column densities (VCDs). The new SCDs are systematically lower (by similar to 10-40 %) than previous, version 2, estimates. Most of this reduction in SCDs is propagated into stratospheric VCDs. Tropospheric NO2 VCDs are also reduced over polluted areas, especially over western Europe, the eastern US, and eastern China. Initial evaluation over unpolluted areas shows that the new SPv3 products agree better with independent satellite- and ground-based Fourier transform infrared (FTIR) measurements. However, further evaluation of tropospheric VCDs is needed over polluted areas, where the increased spatial resolution and more refined AMF estimates may lead to better characterization of pollution hot spots.Keywords:  TROPOSPHERIC NITROGEN-DIOXIDE; ROTATIONAL RAMAN-SCATTERING; SATELLITE MEASUREMENTS; UNITED-STATES; RETRIEVAL ALGORITHM; MULTIANNUAL CHANGES; STRATOSPHERIC NO2; COLUMN RETRIEVAL; CO2 EMISSIONS; POWER-PLANTSYear: 2017Cited: 186Author: Krotkov, Nickolay A. and Lamsal, Lok N. and Celarier, Edward A. and Swartz, William H. and Marchenko, Sergey V. and Bucsela, Eric J. and Chan, Ka Lok and Wenig, Mark and Zara, Marina"
"Title: National ground-level NO<sub>2</sub> predictions via satellite imagery driven convolutional neural networksAbstract: Outdoor air pollution, specifically nitrogen dioxide (NO2), poses a global health risk. Land use regression (LUR) models are widely used to estimate ground-level NO2 concentrations by describing the satellite land use characteristics of a given location using buffer distance averages of variables. However, information may be leaked in this approach as averages ignore the variances within the averaged region. Therefore, in this study, we leverage a convolutional neural network (CNN) architecture to directly pass data grids of various satellite data for the prediction of U.S. national ground-level NO2. We designed CNN architectures of various complexity which inputs both satellite and meteorological reanalysis data, testing both high and low resolution data grids. Our resulting model accurately predicted NO2 concentrations at both daily (R-2 = 0.892, RMSE = 2.259, MAE = 1.534) and annual (R-2 = 0.952, RMSE = 0.988, MAE = 0.690) temporal scales, with coarse resolution imagery and simple CNN architectures displaying the best and most efficient performance. Furthermore, the CNN outperforms traditional buffer distance models, including random forest (RF), feedforward neural network (FNN), and multivariate linear regression (MLR) approaches, resulting in the MLR performing the poorest at daily (R-2 = 0.625, RMSE = 4.281, MAE = 3.102) and annual (R-2 = 0.758, RMSE = 2.218, MAE = 1.652) scales. With the success of the CNN in this approach, satellite land use variables continue to be useful for the prediction of NO2. Using this computationally inexpensive model, we encourage the globalization of advanced LUR models as a low-cost alternative to traditional NO2 monitoring.Keywords: air pollution; convolutional neural networks; land use; environmental modeling; machine learning; nitrogen dioxide USE REGRESSION-MODEL; AIR-QUALITY; NITROGEN-DIOXIDE; POLLUTANTS; RESOLUTION; CHEMISTRY; MORTALITY; PRECURSORYear: 2023Cited: 1Author: Cao, Elton L."
################
Output:
("entity"{tuple_delimiter}"NO2"{tuple_delimiter}"Chemical_species"{tuple_delimiter}"Nitrogen dioxide, a significant air pollutant and a focus of both studies, particularly in measuring its concentration and predicting its levels."){record_delimiter}
("entity"{tuple_delimiter}"OMI"{tuple_delimiter}"Satellite_sensor"{tuple_delimiter}"Ozone Monitoring Instrument, a satellite sensor used for measuring atmospheric components, including NO2, providing data for research."){record_delimiter}
("entity"{tuple_delimiter}"SPv3"{tuple_delimiter}"Technology_algorithm"{tuple_delimiter}"Version 3.0 of the NASA OMI standard NO2 product, which includes improvements in spectral fitting and resolution for NO2 measurements."){record_delimiter}
("entity"{tuple_delimiter}"SCD"{tuple_delimiter}"Retrieval_parameter"{tuple_delimiter}"Slant Column Density, a measurement used in the retrieval of NO2, with improvements in version 3.0 leading to lower estimates."){record_delimiter}
("entity"{tuple_delimiter}"VCD"{tuple_delimiter}"Retrieval_parameter"{tuple_delimiter}"Vertical Column Density, derived from SCD, used to quantify atmospheric NO2, with tropospheric and stratospheric distinctions."){record_delimiter}
("entity"{tuple_delimiter}"GMI"{tuple_delimiter}"Atmospheric_model"{tuple_delimiter}"Global Modeling Initiative, a chemistry-transport model used to provide a priori NO2 and temperature profiles for AMF calculation."){record_delimiter}
("entity"{tuple_delimiter}"AMF"{tuple_delimiter}"Retrieval_parameter"{tuple_delimiter}"Air Mass Factor, used to convert SCDs into VCDs, with calculations refined in SPv3 using GMI model outputs."){record_delimiter}
("entity"{tuple_delimiter}"FTIR"{tuple_delimiter}"Measurement_instrument"{tuple_delimiter}"Fourier Transform Infrared, a ground-based measurement technique used for validating satellite NO2 products."){record_delimiter}
("entity"{tuple_delimiter}"western Europe"{tuple_delimiter}"Location_region"{tuple_delimiter}"A region where tropospheric NO2 VCDs are analyzed, showing reductions in the new SPv3 data."){record_delimiter}
("entity"{tuple_delimiter}"eastern China"{tuple_delimiter}"Location_region"{tuple_delimiter}"A region where tropospheric NO2 VCDs are analyzed, showing reductions in the new SPv3 data."){record_delimiter}
("entity"{tuple_delimiter}"LUR"{tuple_delimiter}"Technology_algorithm"{tuple_delimiter}"Land Use Regression, models used to estimate ground-level NO2 concentrations based on land use characteristics."){record_delimiter}
("entity"{tuple_delimiter}"CNN"{tuple_delimiter}"Technology_algorithm"{tuple_delimiter}"Convolutional Neural Network, an architecture used for predicting ground-level NO2 concentrations from satellite and meteorological data."){record_delimiter}
("entity"{tuple_delimiter}"R-2"{tuple_delimiter}"Result_metric"{tuple_delimiter}"Coefficient of determination, a statistical measure used to evaluate the performance of the CNN model in predicting NO2 concentrations."){record_delimiter}
("entity"{tuple_delimiter}"RMSE"{tuple_delimiter}"Result_metric"{tuple_delimiter}"Root Mean Square Error, a measure of the differences between values predicted by the model and the actual values, used to assess model accuracy."){record_delimiter}
("entity"{tuple_delimiter}"MAE"{tuple_delimiter}"Result_metric"{tuple_delimiter}"Mean Absolute Error, another metric for evaluating the accuracy of the NO2 prediction model."){record_delimiter}
("entity"{tuple_delimiter}"RF"{tuple_delimiter}"Technology_algorithm"{tuple_delimiter}"Random Forest, a traditional machine learning model used for comparison with the CNN in predicting NO2 levels."){record_delimiter}
("entity"{tuple_delimiter}"FNN"{tuple_delimiter}"Technology_algorithm"{tuple_delimiter}"Feedforward Neural Network, a type of neural network model compared against the CNN for NO2 prediction."){record_delimiter}
("entity"{tuple_delimiter}"MLR"{tuple_delimiter}"Technology_algorithm"{tuple_delimiter}"Multivariate Linear Regression, a statistical technique used as a baseline for comparison with more complex models like CNN."){record_delimiter}
("entity"{tuple_delimiter}"US"{tuple_delimiter}"Location_region"{tuple_delimiter}"United States, the area of focus for the national ground-level NO2 prediction study."){record_delimiter}
("entity"{tuple_delimiter}"2017"{tuple_delimiter}"Publication_year"{tuple_delimiter}"The year of publication for the study on the version 3 OMI NO2 standard product."){record_delimiter}
("entity"{tuple_delimiter}"Krotkov, Nickolay A."{tuple_delimiter}"Author"{tuple_delimiter}"Lead author of the study on the version 3 OMI NO2 standard product."){record_delimiter}
("entity"{tuple_delimiter}"Cao, Elton L."{tuple_delimiter}"Author"{tuple_delimiter}"Author of the study on national ground-level NO2 predictions via satellite imagery driven convolutional neural networks."){record_delimiter}
("relationship"{tuple_delimiter}"OMI"{tuple_delimiter}"NO2"{tuple_delimiter}"OMI is used to measure NO2, providing data on its atmospheric concentration."{tuple_delimiter}"measurement, data provision"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"SPv3"{tuple_delimiter}"OMI"{tuple_delimiter}"SPv3 is a product of OMI, representing an improvement in the instrument's data processing and analysis capabilities."{tuple_delimiter}"product development, improvement"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"SCD"{tuple_delimiter}"SPv3"{tuple_delimiter}"SPv3 improves the retrieval of SCD, a key metric for NO2 measurement."{tuple_delimiter}"improvement, data retrieval"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"VCD"{tuple_delimiter}"SCD"{tuple_delimiter}"VCD is derived from SCD, providing a quantitative measure of atmospheric NO2."{tuple_delimiter}"derivation, conversion"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"GMI"{tuple_delimiter}"AMF"{tuple_delimiter}"GMI provides data used in the calculation of AMF, which is essential for converting SCD to VCD."{tuple_delimiter}"data provision, calculation"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"FTIR"{tuple_delimiter}"VCD"{tuple_delimiter}"FTIR measurements are used to validate VCD estimates, ensuring the accuracy of satellite-derived NO2 data."{tuple_delimiter}"validation, accuracy assessment"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"western Europe"{tuple_delimiter}"NO2"{tuple_delimiter}"western Europe is a region where NO2 concentrations are studied, particularly in the context of air pollution."{tuple_delimiter}"study location, concentration analysis"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"eastern US"{tuple_delimiter}"NO2"{tuple_delimiter}"eastern US is a region where NO2 concentrations are studied, with a focus on changes in pollution levels."{tuple_delimiter}"study location, concentration analysis"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"eastern China"{tuple_delimiter}"NO2"{tuple_delimiter}"eastern China is a region where NO2 concentrations are analyzed, particularly in relation to air quality."{tuple_delimiter}"study location, concentration analysis"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"LUR"{tuple_delimiter}"NO2"{tuple_delimiter}"LUR models are used to estimate ground-level NO2 concentrations, linking land use characteristics to air pollution."{tuple_delimiter}"estimation, modeling"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"CNN"{tuple_delimiter}"NO2"{tuple_delimiter}"CNNs are employed to predict ground-level NO2 concentrations, leveraging satellite and meteorological data for improved accuracy."{tuple_delimiter}"prediction, modeling"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"R-2"{tuple_delimiter}"CNN"{tuple_delimiter}"R-2 is used as a metric to evaluate the performance of CNN models in predicting NO2 concentrations."{tuple_delimiter}"evaluation, performance assessment"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"RMSE"{tuple_delimiter}"CNN"{tuple_delimiter}"RMSE is a metric used to assess the accuracy of CNN models in predicting NO2 levels."{tuple_delimiter}"evaluation, accuracy assessment"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"MAE"{tuple_delimiter}"CNN"{tuple_delimiter}"MAE is another metric for evaluating the accuracy of CNN models in NO2 prediction."{tuple_delimiter}"evaluation, accuracy assessment"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"RF"{tuple_delimiter}"CNN"{tuple_delimiter}"RF is compared with CNNs to evaluate their effectiveness in predicting NO2 concentrations."{tuple_delimiter}"comparison, performance evaluation"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"FNN"{tuple_delimiter}"CNN"{tuple_delimiter}"FNN is compared with CNNs to assess their predictive capabilities for NO2 levels."{tuple_delimiter}"comparison, performance evaluation"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"MLR"{tuple_delimiter}"CNN"{tuple_delimiter}"MLR is used as a baseline model for comparison with CNNs in predicting NO2 concentrations."{tuple_delimiter}"comparison, performance evaluation"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"US"{tuple_delimiter}"NO2"{tuple_delimiter}"The US is the geographical focus for the study on predicting national ground-level NO2 concentrations."{tuple_delimiter}"study area, concentration prediction"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Krotkov, Nickolay A."{tuple_delimiter}"2017"{tuple_delimiter}"Krotkov, Nickolay A. is the lead author of the study published in 2017."{tuple_delimiter}"authorship, publication"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Krotkov, Nickolay A."{tuple_delimiter}"SPv3"{tuple_delimiter}"Krotkov, Nickolay A. contributed to the study that describes the SPv3 product."{tuple_delimiter}"contribution, product description"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Cao, Elton L."{tuple_delimiter}"CNN"{tuple_delimiter}"Cao, Elton L. conducted research on using CNNs for predicting NO2 concentrations."{tuple_delimiter}"research, methodology development"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"NO2 measurement, satellite data, air pollution, model evaluation, convolutional neural networks, land use regression"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [Chemical_species, Satellite_sensor, Measurement_instrument, Atmospheric_model, Radiation_model, Retrieval_parameter, Technology_algorithm, Result_metric, Policy_regulation, Research_project, Location_region, Temporal_period, Spatial_resolution, Temporal_resolution, Author, Publication_year]
Text:
"Title: Multi-faceted analysis of dust storm from satellite imagery, ground station, and model simulations, a study in China
Abstract: An intense dust storm from 8 April to 11 April 2023 originated from the Gobi deserts bordering Mongolia and Inner Mongolia of China and affected most parts of northern, central, and eastern China, the Korean Peninsula, and Japan. It has a significant impact on air quality in these regions and alters the optical and microphysical properties of the aerosols. In this work, a comprehensive analysis of the storm was carried out by using reanalysis data, model simulation, satellite, and ground-based observations. The geopotential height along with the wind flow reveals that the development, transportation, and dissipation of the dust storms were closely related to the movement of the Mongolia cyclones caused by Mongolia low and its surrounding highs. The Cloud-Aerosol Lidar and Infrared Pathfinder Satellite Observation (CALIPSO) data showed a two-layer dust vertical distribution, with the bottom one below 5 km and the upper one stretching from 5 to 10 km over the Japan Sea. The Hybrid SingleParticle Lagrangian Integrated Trajectory model (HYSPLIT) backward trajectory uncovered Central Mongolia being the origin of the dust storm that arrived over the Japan Sea on April 9, 2022, and the forward trajectory revealed that the dust aerosols would be further transported to the Pacific Ocean. Air quality analysis demonstrated that the regions of inner Mongolia (IMG) and Jing-Jin-Ji (JJJ) suffered the most from the dust storm events, followed by the Yangtze River Delta (YRD), while the Pearl River Delta (PRD) was hardly affected, as indicated by the regional-averaged PM10 and PM2.5. It was also found that the dust storm event has almost no significant influence on the other air quality indicators including CO, NO2, O3, and SO2. Historical record tracking revealed that the springtime averaged PM10 and PM2.5 of the year 2023 are comparable to those in 2021 which has the record-breaking dust storm case. AERONET data indicated dramatic increments of aerosol optical depth at 550 nm (AOD550) and effective radius of total size (ReffT) in regions of Gobi and JJJ, accompanied by low Angstrom Exponent (AE), and high SSA870 values, while in the regions of Korea and Japan, minor increments of AOD550 and ReffT were found. This study provides a holistic scientific view of the dust storm which could aid in the implementation of protective measures against dust storms.
Keywords: Dust storm; HYSPLIT; Satellite observation; Air quality; Aerosol optical depth MINERAL DUST; RADIATIVE PROPERTIES; EVENTS; AEROSOLS; CLIMATE; HEALTH; IMPACT; SIZE
Year: 2024
Cited: 0
Author: Li, Jing and Wong, Man Sing and Shi, Guoqiang"
"Title: A high-resolution and observationally constrained OMI NO<sub>2</sub> satellite retrieval
Abstract: This work presents a new high-resolution NO2 dataset derived from the NASA Ozone Monitoring Instrument (OMI) NO2 version 3.0 retrieval that can be used to estimate surface-level concentrations. The standard NASA product uses NO2 vertical profile shape factors from a 1.25 degrees x 1 degrees (similar to 110 km x 110 km) resolution Global Model Initiative (GMI) model simulation to calculate air mass factors, a critical value used to determine observed tropospheric NO2 vertical columns. To better estimate vertical profile shape factors, we use a high-resolution (1.33 km x 1.33 km) Community Multi-scale Air Quality (CMAQ) model simulation constrained by in situ aircraft observations to recalculate tropospheric air mass factors and tropospheric NO2 vertical columns during summertime in the eastern US. In this new product, OMI NO2 tropospheric columns increase by up to 160% in city centers and decrease by 20-50% in the rural areas outside of urban areas when compared to the operational NASA product. Our new product shows much better agreement with the Pandora NO2 and Airborne Compact Atmospheric Mapper (ACAM) NO2 spectrometer measurements acquired during the DISCOVER-AQ Maryland field campaign. Furthermore, the correlation between our satellite product and EPA NO2 monitors in urban areas has improved dramatically: r(2) = 0.60 in the new product vs. r(2) = 0.39 in the operational product, signifying that this new product is a better indicator of surface concentrations than the operational product. Our work emphasizes the need to use both high-resolution and high-fidelity models in order to recalculate satellite data in areas with large spatial heterogeneities in NO x emissions. Although the current work is focused on the eastern US, the methodology developed in this work can be applied to other world regions to produce high-quality region-specific NO2 satellite retrievals.
Keywords:  EASTERN UNITED-STATES; LAND-USE REGRESSION; GROUND-BASED MEASUREMENTS; TROPOSPHERIC NO2; DISCOVER-AQ; AIR-QUALITY; COLUMN DENSITIES; INTEX-B; DOAS MEASUREMENTS; NITROGEN-DIOXIDE
Year: 2017
Cited: 53
Author: Goldberg, Daniel L. and Lamsal, Lok N. and Loughner, Christopher P. and Swartz, William H. and Lu, Zifeng and Streets, David G."
"Title: Characterization of ozone in the lower troposphere during the 2016 G20 conference in Hangzhou
Abstract: Recently, atmospheric ozone pollution has demonstrated an aggravating tendency in China. To date, most research about atmospheric ozone has been confined near the surface, and an understanding of the vertical ozone structure is limited. During the 2016 G20 conference, strict emission control measures were implemented in Hangzhou, a megacity in the Yangtze River Delta, and its surrounding regions. Here, we monitored the vertical profiles of ozone concentration and aerosol extinction coefficients in the lower troposphere using an ozone lidar, in addition to the vertical column densities (VCDs) of ozone and its precursors in the troposphere through satellite-based remote sensing. The ozone concentrations reached a peak near the top of the boundary layer. During the control period, the aerosol extinction coefficients in the lower lidar layer decreased significantly; however, the ozone concentration fluctuated frequently with two pollution episodes and one clean episode. The sensitivity of ozone production was mostly within VOC-limited or transition regimes, but entered a NOx-limited regime due to a substantial decline of NOx during the clean episode. Temporary measures took no immediate effect on ozone pollution in the boundary layer; instead, meteorological conditions like air mass sources and solar radiation intensities dominated the variations in the ozone concentration.
Keywords:  BOUNDARY-LAYER OZONE; NORTHERN CHINA; UNITED-STATES; SURFACE OZONE; COLUMN OZONE; POLLUTION; LIDAR; NO2; SENSITIVITY; REACTIVITY
Year: 2017
Cited: 68
Author: Su, Wenjing and Liu, Jianguo"
#############
Output:
("entity"{tuple_delimiter}"dust storm"{tuple_delimiter}"Chemical_species"{tuple_delimiter}"Dust storms are significant atmospheric events characterized by the lifting and transport of dust particles, affecting air quality and aerosol properties."){record_delimiter}
("entity"{tuple_delimiter}"PM10"{tuple_delimiter}"Chemical_species"{tuple_delimiter}"Particulate matter with a diameter of 10 micrometers or less, a key indicator of air quality, significantly impacted by dust storms."){record_delimiter}
("entity"{tuple_delimiter}"PM2.5"{tuple_delimiter}"Chemical_species"{tuple_delimiter}"Particulate matter with a diameter of 2.5 micrometers or less, another critical air quality indicator, also affected by dust storm events."){record_delimiter}
("entity"{tuple_delimiter}"CO"{tuple_delimiter}"Chemical_species"{tuple_delimiter}"Carbon monoxide, an air quality indicator measured during the dust storm, showing no significant influence from the event."){record_delimiter}
("entity"{tuple_delimiter}"NO2"{tuple_delimiter}"Chemical_species"{tuple_delimiter}"Nitrogen dioxide, an air pollutant monitored for its concentration changes, with the dust storm having no significant impact on its levels. Also focused in another paper as a key species to be retrieved."){record_delimiter}
("entity"{tuple_delimiter}"O3"{tuple_delimiter}"Chemical_species"{tuple_delimiter}"Ozone, an air quality indicator, with no significant changes observed due to the dust storm. In another paper, it is the key species to be studied."){record_delimiter}
("entity"{tuple_delimiter}"SO2"{tuple_delimiter}"Chemical_species"{tuple_delimiter}"Sulfur dioxide, an air pollutant measured, with the dust storm not significantly affecting its concentration."){record_delimiter}
("entity"{tuple_delimiter}"CALIPSO"{tuple_delimiter}"Satellite_sensor"{tuple_delimiter}"Cloud-Aerosol Lidar and Infrared Pathfinder Satellite Observation, used for observing the vertical distribution of dust during the storm."){record_delimiter}
("entity"{tuple_delimiter}"OMI"{tuple_delimiter}"Satellite_sensor"{tuple_delimiter}"Ozone Monitoring Instrument, used for NO2 retrieval in the study, providing data for estimating surface-level concentrations."){record_delimiter}
("entity"{tuple_delimiter}"HYSPLIT"{tuple_delimiter}"Atmospheric_model"{tuple_delimiter}"Hybrid Single-Particle Lagrangian Integrated Trajectory model, used to trace the origin and transport path of the dust storm."){record_delimiter}
("entity"{tuple_delimiter}"GMI"{tuple_delimiter}"Atmospheric_model"{tuple_delimiter}"Global Model Initiative model, used in the standard NASA product for calculating air mass factors in NO2 retrieval."){record_delimiter}
("entity"{tuple_delimiter}"CMAQ"{tuple_delimiter}"Atmospheric_model"{tuple_delimiter}"Community Multi-scale Air Quality model, used for high-resolution simulation to recalculate tropospheric air mass factors and NO2 vertical columns."){record_delimiter}
("entity"{tuple_delimiter}"AOD550"{tuple_delimiter}"Retrieval_parameter"{tuple_delimiter}"Aerosol optical depth at 550 nm, an indicator of aerosol loading, showing dramatic increments in certain regions during the dust storm."){record_delimiter}
("entity"{tuple_delimiter}"ReffT"{tuple_delimiter}"Retrieval_parameter"{tuple_delimiter}"Effective radius of total size, a parameter indicating the size of aerosol particles, also showing changes during the dust storm."){record_delimiter}
("entity"{tuple_delimiter}"AE"{tuple_delimiter}"Retrieval_parameter"{tuple_delimiter}"Angstrom Exponent, a parameter related to the size distribution of aerosols, showing low values during the dust storm, indicating larger particles."){record_delimiter}
("entity"{tuple_delimiter}"SSA870"{tuple_delimiter}"Retrieval_parameter"{tuple_delimiter}"Single Scattering Albedo at 870 nm, indicating the scattering properties of aerosols, with high values during the dust storm."){record_delimiter}
("entity"{tuple_delimiter}"Pandora"{tuple_delimiter}"Measurement_instrument"{tuple_delimiter}"A spectrometer used for measuring NO2, providing validation for the new OMI NO2 product."){record_delimiter}
("entity"{tuple_delimiter}"ACAM"{tuple_delimiter}"Measurement_instrument"{tuple_delimiter}"Airborne Compact Atmospheric Mapper, a spectrometer used for NO2 measurements, validating the new OMI NO2 product."){record_delimiter}
("entity"{tuple_delimiter}"Gobi deserts"{tuple_delimiter}"Location_region"{tuple_delimiter}"The origin of the dust storm, located on the border of Mongolia and Inner Mongolia of China."){record_delimiter}
("entity"{tuple_delimiter}"Korean Peninsula"{tuple_delimiter}"Location_region"{tuple_delimiter}"A region affected by the dust storm."){record_delimiter}
("entity"{tuple_delimiter}"Japan"{tuple_delimiter}"Location_region"{tuple_delimiter}"A region affected by the dust storm, particularly the Japan Sea area."){record_delimiter}
("entity"{tuple_delimiter}"Central Mongolia"{tuple_delimiter}"Location_region"{tuple_delimiter}"Identified as the origin of the dust storm that arrived over the Japan Sea."){record_delimiter}
("entity"{tuple_delimiter}"YRD"{tuple_delimiter}"Location_region"{tuple_delimiter}"Yangtze River Delta, a region less affected by the dust storm compared to IMG and JJJ."){record_delimiter}
("entity"{tuple_delimiter}"Gobi"{tuple_delimiter}"Location_region"{tuple_delimiter}"Regions of Gobi showing dramatic increments of AOD550 and ReffT during the dust storm."){record_delimiter}
("entity"{tuple_delimiter}"Korea"{tuple_delimiter}"Location_region"{tuple_delimiter}"Regions of Korea showing minor increments of AOD550 and ReffT during the dust storm."){record_delimiter}
("entity"{tuple_delimiter}"eastern US"{tuple_delimiter}"Location_region"{tuple_delimiter}"Area of focus for the study on high-resolution NO2 retrieval using OMI data."){record_delimiter}
("entity"{tuple_delimiter}"city centers"{tuple_delimiter}"Location_region"{tuple_delimiter}"Urban areas where OMI NO2 tropospheric columns increase significantly in the new product."){record_delimiter}
("entity"{tuple_delimiter}"rural areas"{tuple_delimiter}"Location_region"{tuple_delimiter}"Areas outside of urban centers where OMI NO2 tropospheric columns decrease in the new product."){record_delimiter}
("entity"{tuple_delimiter}"urban areas"{tuple_delimiter}"Location_region"{tuple_delimiter}"Areas where the correlation between the satellite product and EPA NO2 monitors is analyzed."){record_delimiter}
("entity"{tuple_delimiter}"Hangzhou"{tuple_delimiter}"Location_region"{tuple_delimiter}"A megacity in the Yangtze River Delta where strict emission control measures were implemented during the 2016 G20 conference."){record_delimiter}
("entity"{tuple_delimiter}"Yangtze River Delta"{tuple_delimiter}"Location_region"{tuple_delimiter}"A region in China where Hangzhou is located, subject to emission control measures during the 2016 G20 conference."){record_delimiter}
("entity"{tuple_delimiter}"8 April to 11 April 2023"{tuple_delimiter}"Temporal_period"{tuple_delimiter}"The period of the intense dust storm, originating from the Gobi deserts and affecting various regions."){record_delimiter}
("entity"{tuple_delimiter}"April 9, 2022"{tuple_delimiter}"Temporal_period"{tuple_delimiter}"The date when the dust storm arrived over the Japan Sea, as traced by the HYSPLIT model."){record_delimiter}
("entity"{tuple_delimiter}"springtime of the year 2023"{tuple_delimiter}"Temporal_period"{tuple_delimiter}"The period showing comparable PM10 and PM2.5 levels to those in 2021, a year with a record-breaking dust storm case."){record_delimiter}
("entity"{tuple_delimiter}"summertime"{tuple_delimiter}"Temporal_period"{tuple_delimiter}"The season focused on for recalculating tropospheric air mass factors and NO2 vertical columns in the eastern US."){record_delimiter}
("entity"{tuple_delimiter}"G20 conference"{tuple_delimiter}"Policy_regulation"{tuple_delimiter}"The period during which strict emission control measures were implemented in Hangzhou and its surrounding regions."){record_delimiter}
("entity"{tuple_delimiter}"1.33 km x 1.33 km"{tuple_delimiter}"Spatial_resolution"{tuple_delimiter}"High-resolution used in the CMAQ model simulation for recalculating tropospheric air mass factors."){record_delimiter}
("entity"{tuple_delimiter}"2017"{tuple_delimiter}"Publication_year"{tuple_delimiter}"The publication year of the study on high-resolution and observationally constrained OMI NO2 satellite retrieval and the study about ozone in the lower troposphere during the 2016 G20 conference in Hangzhou") {record_delimiter}
("entity"{tuple_delimiter}"Li, Jing"{tuple_delimiter}"Author"{tuple_delimiter}"One of the authors of the study on the multi-faceted analysis of the dust storm."){record_delimiter}
("entity"{tuple_delimiter}"Wong, Man Sing"{tuple_delimiter}"Author"{tuple_delimiter}"One of the authors of the study on the multi-faceted analysis of the dust storm."){record_delimiter}
("entity"{tuple_delimiter}"Shi, Guoqiang"{tuple_delimiter}"Author"{tuple_delimiter}"One of the authors of the study on the multi-faceted analysis of the dust storm."){record_delimiter}
("entity"{tuple_delimiter}"Goldberg, Daniel L."{tuple_delimiter}"Author"{tuple_delimiter}"One of the authors of the study on high-resolution and observationally constrained OMI NO2 satellite retrieval."){record_delimiter}
("entity"{tuple_delimiter}"Lamsal, Lok N."{tuple_delimiter}"Author"{tuple_delimiter}"One of the authors of the study on high-resolution and observationally constrained OMI NO2 satellite retrieval."){record_delimiter}
("entity"{tuple_delimiter}"Loughner, Christopher P."{tuple_delimiter}"Author"{tuple_delimiter}"One of the authors of the study on high-resolution and observationally constrained OMI NO2 satellite retrieval."){record_delimiter}
("entity"{tuple_delimiter}"Swartz, William H."{tuple_delimiter}"Author"{tuple_delimiter}"One of the authors of the study on high-resolution and observationally constrained OMI NO2 satellite retrieval."){record_delimiter}
("entity"{tuple_delimiter}"Lu, Zifeng"{tuple_delimiter}"Author"{tuple_delimiter}"One of the authors of the study on high-resolution and observationally constrained OMI NO2 satellite retrieval."){record_delimiter}
("entity"{tuple_delimiter}"Streets, David G."{tuple_delimiter}"Author"{tuple_delimiter}"One of the authors of the study on high-resolution and observationally constrained OMI NO2 satellite retrieval."){record_delimiter}
("entity"{tuple_delimiter}"Su, Wenjing"{tuple_delimiter}"Author"{tuple_delimiter}"An author of the study on the characterization of ozone during the 2016 G20 conference."){record_delimiter}
("entity"{tuple_delimiter}"Liu, Jianguo"{tuple_delimiter}"Author"{tuple_delimiter}"An author of the study on the characterization of ozone during the 2016 G20 conference."){record_delimiter}
("relationship"{tuple_delimiter}"dust storm"{tuple_delimiter}"northern China"{tuple_delimiter}"Northern China was affected by the dust storm, demonstrating the impact of the storm on the region's air quality."{tuple_delimiter}"impact, affect"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"dust storm"{tuple_delimiter}"Korean Peninsula"{tuple_delimiter}"The Korean Peninsula experienced the effects of the dust storm, highlighting the transboundary nature of such events."{tuple_delimiter}"impact, affect"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"CALIPSO"{tuple_delimiter}"dust storm"{tuple_delimiter}"CALIPSO provided data on the vertical distribution of the dust storm, showcasing the satellite's capability in observing such atmospheric events."{tuple_delimiter}"observation, data provision"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"HYSPLIT"{tuple_delimiter}"dust storm"{tuple_delimiter}"The HYSPLIT model traced the dust storm's origin and transport path, indicating its utility in understanding the dynamics of dust storms."{tuple_delimiter}"modeling, analysis"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"dust storm"{tuple_delimiter}"Central Mongolia"{tuple_delimiter}"HYSPLIT model identified Central Mongolia as the origin of the dust storm that reached the Japan Sea, linking the location to the event."{tuple_delimiter}"source, origin identification"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"dust storm"{tuple_delimiter}"ReffT"{tuple_delimiter}"Increments of ReffT were observed during the dust storm, suggesting changes in aerosol size distribution."{tuple_delimiter}"increase, correlation"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"dust storm"{tuple_delimiter}"AE"{tuple_delimiter}"Low AE values during the dust storm indicated the presence of larger dust particles, affecting the aerosol size distribution."{tuple_delimiter}"correlation, indication"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"dust storm"{tuple_delimiter}"SSA870"{tuple_delimiter}"High SSA870 values during the dust storm suggest enhanced scattering properties of aerosols due to dust particles."{tuple_delimiter}"correlation, indication"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"dust storm"{tuple_delimiter}"PM10"{tuple_delimiter}"The dust storm significantly impacted PM10 levels, especially in regions like IMG and JJJ, showing a direct link between the event and air quality degradation."{tuple_delimiter}"impact, increase"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"8 April to 11 April 2023"{tuple_delimiter}"dust storm"{tuple_delimiter}"This period marked the occurrence of the intense dust storm, defining the temporal scope of the event."{tuple_delimiter}"event period, definition"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"April 9, 2022"{tuple_delimiter}"dust storm"{tuple_delimiter}"The dust storm arrived over the Japan Sea on this date, indicating a specific point in the event's timeline."{tuple_delimiter}"event milestone, arrival"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"springtime of the year 2023"{tuple_delimiter}"PM10"{tuple_delimiter}"The springtime of 2023 showed comparable PM10 levels to 2021, suggesting similar air quality conditions regarding this pollutant."{tuple_delimiter}"comparison, similarity"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Li, Jing"{tuple_delimiter}"2024"{tuple_delimiter}"Li, Jing is an author of the study published in 2024, linking the researcher to their work and its publication date."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Wong, Man Sing"{tuple_delimiter}"2024"{tuple_delimiter}"Wong, Man Sing co-authored the study published in 2024, establishing their contribution to the research and its publication timeline."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Shi, Guoqiang"{tuple_delimiter}"2024"{tuple_delimiter}"Shi, Guoqiang is also an author of the study from 2024, highlighting their involvement in the research and its publication."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"OMI"{tuple_delimiter}"NO2"{tuple_delimiter}"OMI is used for NO2 retrieval, indicating the instrument's role in measuring and analyzing nitrogen dioxide levels."{tuple_delimiter}"measurement, data provision"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"GMI"{tuple_delimiter}"OMI"{tuple_delimiter}"GMI is used in the standard NASA product for calculating air mass factors, which are crucial for OMI's NO2 retrieval process."{tuple_delimiter}"model, calculation"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"CMAQ"{tuple_delimiter}"OMI"{tuple_delimiter}"CMAQ provides high-resolution simulations to improve OMI's NO2 retrieval, especially in areas with significant spatial heterogeneities in emissions."{tuple_delimiter}"model, improvement"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"1.33 km x 1.33 km"{tuple_delimiter}"CMAQ"{tuple_delimiter}"This high resolution is used in the CMAQ model, indicating the detailed scale at which the model operates to enhance NO2 retrieval accuracy."{tuple_delimiter}"resolution, model operation"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"OMI"{tuple_delimiter}"eastern US"{tuple_delimiter}"OMI data is used to study NO2 levels in the eastern US, demonstrating the application of satellite data in regional air quality analysis."{tuple_delimiter}"application, regional study"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"city centers"{tuple_delimiter}"NO2"{tuple_delimiter}"City centers show increased OMI NO2 tropospheric columns, indicating higher pollution levels in urban areas."{tuple_delimiter}"increase, pollution indication"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"rural areas"{tuple_delimiter}"NO2"{tuple_delimiter}"Rural areas exhibit decreased OMI NO2 tropospheric columns, suggesting lower pollution levels compared to urban centers."{tuple_delimiter}"decrease, pollution indication"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Pandora"{tuple_delimiter}"OMI"{tuple_delimiter}"Pandora NO2 measurements are used to validate the new OMI NO2 product, ensuring the accuracy of the satellite-derived data."{tuple_delimiter}"validation, accuracy assurance"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"ACAM"{tuple_delimiter}"OMI"{tuple_delimiter}"ACAM measurements also validate the new OMI NO2 product, further confirming the reliability of the satellite data."{tuple_delimiter}"validation, reliability confirmation"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Goldberg, Daniel L."{tuple_delimiter}"2017"{tuple_delimiter}"Goldberg, Daniel L. is an author of the study published in 2017, linking the researcher to their work and its publication date."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Lamsal, Lok N."{tuple_delimiter}"2017"{tuple_delimiter}"Lamsal, Lok N. co-authored the study published in 2017, establishing their contribution to the research and its publication timeline."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Loughner, Christopher P."{tuple_delimiter}"2017"{tuple_delimiter}"Loughner, Christopher P. is also an author of the 2017 study, highlighting their involvement in the research and its publication."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Swartz, William H."{tuple_delimiter}"2017"{tuple_delimiter}"Swartz, William H. is another author of the study from 2017, indicating their role in the research and its publication."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Lu, Zifeng"{tuple_delimiter}"2017"{tuple_delimiter}"Lu, Zifeng contributed to the 2017 study, linking them to the research work and its publication date."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Streets, David G."{tuple_delimiter}"2017"{tuple_delimiter}"Streets, David G. is an author of the 2017 study, highlighting their participation in the research and its publication."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"ozone lidar"{tuple_delimiter}"O3"{tuple_delimiter}"Ozone lidar is used to monitor vertical profiles of ozone, indicating its capability in measuring ozone concentration in the lower troposphere."{tuple_delimiter}"measurement, monitoring"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"G20 conference"{tuple_delimiter}"Hangzhou"{tuple_delimiter}"Strict emission control measures were implemented in Hangzhou during the 2016 G20 conference, demonstrating a policy intervention aimed at improving air quality."{tuple_delimiter}"policy intervention, air quality improvement"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"G20 conference"{tuple_delimiter}"Yangtze River Delta"{tuple_delimiter}"The Yangtze River Delta region, including Hangzhou, was subject to emission control measures during the 2016 G20 conference, indicating a regional approach to air quality management."{tuple_delimiter}"policy intervention, regional management"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Su, Wenjing"{tuple_delimiter}"2017"{tuple_delimiter}"Su, Wenjing is an author of the study published in 2017, linking the researcher to their work on ozone characterization during the 2016 G20 conference."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Liu, Jianguo"{tuple_delimiter}"2017"{tuple_delimiter}"Liu, Jianguo co-authored the study published in 2017, establishing their contribution to the research on ozone during the 2016 G20 conference."{tuple_delimiter}"authorship, publication year"{tuple_delimiter}10){record_delimiter}
("content_keywords"{tuple_delimiter}"dust storm, air quality, satellite observation, model simulation, aerosol properties, emission control, ozone, NO2, high-resolution retrieval"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are an expert in Bibliometrics and Knowledge Graph. You are skilled at network analysis, citation mapping, and data visualization, with a strong background in atmospheric environmental remote sensing. 
You are adept at helping people with identifying research trends, patterns, and relationships within the Web of Science index, particularly in the academic research domain of atmospheric environmental remote sensing. 
You can provide valuable insights into the community structure and knowledge dynamics of this field, enabling informed decision-making and research strategy development.
Using your expertise, you're asked to generate a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.
Enrich it as much as you can with relevant information from the nearby text, this is very important.
If no answer is possible, or the description is empty, only convey information that is provided within the text.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Data tables---

{context_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to questions about documents provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Documents---

{content_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate the following two points and provide a similarity score between 0 and 1 directly:
1. Whether these two questions are semantically similar
2. Whether the answer to Question 2 can be used to answer Question 1
Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""
