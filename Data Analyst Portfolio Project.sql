USE PorfolioProject

SELECT *
FROM PorfolioProject..covidDeaths
WHERE continent IS NOT NULL
order by 3,4

--SELECT *
--FROM PorfolioProject..covidVaccinations
--order by 3,4

--Select the Data that we are going to be using

--SELECT Location, date, total_cases, new_cases, total_deaths, population
--FROM PorfolioProject..covidDeaths
--WHERE continent IS NOT NULL
--ORDER BY 1

-- Looking at Total Cases vs Total Deaths
-- Shows the likelihood of dying if you cntract Covid in your country
SELECT Location, CONVERT (date, date,105) as date, total_cases, new_cases, total_deaths, (CAST(total_deaths as float)/CAST(total_cases as float))*100 as DeathPercentage
FROM PorfolioProject..covidDeaths
WHERE total_cases > 0 AND location LIKE '%Trinidad%' AND continent IS NOT NULL
ORDER BY 1,2

-- Looking at the total cases vs population
--Shows what percentage of the population got Covid
SELECT Location, CONVERT (date, date,105) as date, population, total_cases, (CAST(total_deaths as float)/CAST(population as float))*100 as PercentPopulationInfected
FROM PorfolioProject..covidDeaths
WHERE total_cases > 0 AND location LIKE '%Trinidad%' AND continent IS NOT NULL
ORDER BY 1,2


-- Looking at countries with highest infection rate compared to population

SELECT Location, population, MAX(total_cases) as HighestInfectionCount, MAX((CAST(total_cases as float)/CAST(population as float)))*100 as PercentPopulationInfected
FROM PorfolioProject..covidDeaths
WHERE continent IS NOT NULL
GROUP BY Location, population
ORDER BY 4 DESC

-- Showing the countires with the highest death count per popluation

SELECT Location, MAX(CAST(total_deaths as INT)) as TotalDeathCount
FROM PorfolioProject..covidDeaths
WHERE continent <> ' '
GROUP BY Location
ORDER BY 2 DESC

--LET'S BREAK THINGS DOWN BY CONTINENT
-- not correct as the data may not be grouped properly
SELECT continent, MAX(CAST(total_deaths as INT)) as TotalDeathCount
FROM PorfolioProject..covidDeaths
WHERE continent <> ' '
GROUP BY continent
ORDER BY 2 DESC

--LET'S BREAK THINGS DOWN BY LOCATION

SELECT location, MAX(CAST(total_deaths as INT)) as TotalDeathCount
FROM PorfolioProject..covidDeaths
WHERE continent = ' '
GROUP BY location
ORDER BY 2 DESC

--Showing the continent with the highest death count per population

SELECT continent, MAX(CAST(total_deaths as INT)) as TotalDeathCount
FROM PorfolioProject..covidDeaths
WHERE continent <> ' ' 
GROUP BY continent
ORDER BY 2 DESC


-- GLOBAL NUMBERS
-- Covid deaths percentages GLOBALLY
SELECT CONVERT (date, date,105) as date, SUM(CAST(new_cases AS int)) as total_new_cases, SUM(CAST(new_deaths as INT)) as total_new_deaths, (SUM(CAST(new_deaths as float))/SUM(CAST(new_cases AS float)))*100 AS deathPercentage
FROM PorfolioProject..covidDeaths
WHERE continent <> ' ' AND new_cases > 0 AND new_deaths > 0
GROUP BY date
ORDER BY 1,2


--Showing Vaccination numbers GLOBALLY
SELECT dea.continent, dea.location, CONVERT(date, dea.date, 105) as date, dea.population, vac.new_vaccinations
FROM PorfolioProject..covidDeaths dea JOIN PorfolioProject..covidVaccinations vac
	ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent <> ''
ORDER BY 2,3

--Rolling average for new vaccinations
SELECT dea.continent, dea.location, CONVERT(date, dea.date, 105) as date, dea.population, CONVERT(float,vac.new_vaccinations) as new_vaccinations, SUM(CONVERT(float, vac.new_vaccinations)) OVER (Partition BY dea.Location ORDER BY dea.Location,CONVERT(date, dea.date, 105)) as RollingPeopleVaccinated
FROM PorfolioProject..covidDeaths dea JOIN PorfolioProject..covidVaccinations vac
	ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent <> ''
ORDER BY 2,3



-- USING CTE

WITH PopvsVac (continent, location, date, population, new_vaccinations, RollingPeopleVaccinated)
   as
(
SELECT dea.continent, dea.location, CONVERT(date, dea.date, 105) as date, CAST(dea.population as float), CONVERT(float,vac.new_vaccinations) as new_vaccinations, SUM(CONVERT(float, vac.new_vaccinations)) OVER (Partition BY dea.Location ORDER BY dea.Location,CONVERT(date, dea.date, 105)) as RollingPeopleVaccinated
FROM PorfolioProject..covidDeaths dea JOIN PorfolioProject..covidVaccinations vac
	ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent <> ''
--ORDER BY 2,3
)
SELECT *, (RollingPeopleVaccinated/population)*100 as RollingPeopleVaccinatedPercent
FROM PopvsVac
--WHERE location LIKE '%Trinidad%'


--TEMP TABLE
DROP TABLE if exists #PercentPopulationVaccinated
Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)

INSERT INTO #PercentPopulationVaccinated
SELECT dea.continent, dea.location, CONVERT(date, dea.date, 105) as date, CAST(dea.population as float) as population, CONVERT(float,vac.new_vaccinations) as new_vaccinations, SUM(CONVERT(float, vac.new_vaccinations)) OVER (Partition BY dea.Location ORDER BY dea.Location,CONVERT(date, dea.date, 105)) as RollingPeopleVaccinated
FROM PorfolioProject..covidDeaths dea JOIN PorfolioProject..covidVaccinations vac
	ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent <> ''
--ORDER BY 2,3

SELECT *, (RollingPeopleVaccinated/population)*100 as RollingPeopleVaccinatedPercent
FROM #PercentPopulationVaccinated
WHERE location LIKE '%Trinidad%'


--creating view to store data for later visualizations

CREATE VIEW PercentPopulationVaccinated as 
SELECT dea.continent, dea.location, CONVERT(date, dea.date, 105) as date, CAST(dea.population as float) as population, CONVERT(float,vac.new_vaccinations) as new_vaccinations, SUM(CONVERT(float, vac.new_vaccinations)) OVER (Partition BY dea.Location ORDER BY dea.Location,CONVERT(date, dea.date, 105)) as RollingPeopleVaccinated
FROM PorfolioProject..covidDeaths dea JOIN PorfolioProject..covidVaccinations vac
	ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent <> ''
--ORDER BY 2,3

