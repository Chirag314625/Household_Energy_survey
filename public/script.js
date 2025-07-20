// Add these new variable declarations at the top of script.js
const surveyContainer = document.getElementById("surveyContainer");
const thankYouMessage = document.getElementById("thankYouMessage");

document.addEventListener("DOMContentLoaded", function() {
    let questions = [
      // General & Household Demographics
      {
        text: "What is your name?",
        input: "text",
        placeholder: "Your full name",
        name: "name",
        id: 0
      },
      {
        text: "What is your city and pincode?",
        input: "multiple",
        inputs: [
          { name: "City", placeholder: "City / Village", type: "text" },
          { name: "Pincode", placeholder: "Pincode", type: "text", pattern: "^\\d{6}$", validationMessage: "Please enter a valid 6-digit numeric Pincode." }
        ],
        id: 1
      },
      {
        text: "How many members of your household are adults (18 years of age or older)?",
        input: "number",
        placeholder: "Number of adults",
        min: "0",
        step: "1",
        name: "num_adults",
        id: 2
      },

      // Home Characteristics
      {
        text: "Which best describes your home?",
        options: [
          "Mobile home",
          "Single-family house detached from any other house",
          "Single-family house attached to one or more other houses (for example: duplex, row house, or townhome)",
          "Apartment in a building with 2 to 4 units",
          "Apartment in a building with 5 or more units"
        ],
        name: "home_type",
        id: 3
      },
      {
        text: "Do you own or rent your home?",
        options: ["Own", "Rent"],
        name: "ownership",
        id: 4 // Dependent question for 'year_built' and 'move_in_year'
      },
      {
        text: "When was your home built?",
        options: ["Before 1970", "1970 to 1979", "1980 to 1989", "1990 to 1999", "2000 to 2009", "2010 to 2019", "2020 to present"],
        condition: { questionId: 4, value: "Own" },
        name: "year_built",
        id: 5
      },
      {
        text: "When did your household move in?",
        options: ["Before 1970", "1970 to 1979", "1980 to 1989", "1990 to 1999", "2000 to 2009", "2010 to 2019", "2020 to present"],
        condition: { questionId: 4, value: "Rent" },
        name: "move_in_year",
        id: 6
      },{
        text: "What is the approximate square footage of your home? If you do not know, please enter your best estimate. If you live in an apartment, please include the square footage of your unit only, not the entire building.",
        input: "number",
        placeholder: "Square footage",
        min: "0",
        step: "1",
        name: "sq_ft_home",
        id: 7
      },
      {
        text: "Which of the following areas are included in your estimate of square footage?",
        type: "checkbox", // This is actually a radio group based on your render logic
        sections: [
          {
            title: "A. Basement",
            name: "sq_ft_basement",
            options: ["Yes", "No", "Don't know", "Not applicable (my home does not have this space)"]
          },
          {
            title: "B. Attic",
            name: "sq_ft_attic",
            options: ["Yes", "No", "Don't know", "Not applicable (my home does not have this space)"]
          },
          {
            title: "C. Attached garage",
            name: "sq_ft_garage",
            options: ["Yes", "No", "Don't know", "Not applicable (my home does not have this space)"]
          }
        ],
        id: 8
      },

      // Kitchen Appliances
      {
        text: "How many refrigerators(fridge) are plugged-in and turned on in your home? Include refrigerators in basements or garages, even if they are only used occasionall. If none, please enter \"0.\"",
        input: "number",
        placeholder: "Number of refrigerators",
        min: "0",
        step: "1",
        name: "num_refrigerators",
        id: 9 // Dependent question for 'refrigerator_size', 'refrigerator_type', 'refrigerator_age'
      },
      {
        text: "What is the size of your most used refrigerator?",
        options: [
          "Half-size or compact",
          "Small (17.5 cubic feet or less)",
          "Medium (17.6 to 22.5 cubic feet)",
          "Large (22.6 to 29.5 cubic feet)",
          "Very large (bigger than 29.5 cubic feet)"
        ],
        condition: { questionId: 9, operator: "greater", value: 0 },
        name: "refrigerator_size",
        id: 10
      },
      {
        text: "Which of the following best describes your most used refrigerator?",
        options: [
          "One door",
          "Two doors, freezer next to the refrigerator",
          "Two doors, freezer above the refrigerator",
          "Two doors, freezer below the refrigerator",
          "Three or more doors"
        ],
        condition: { questionId: 9, operator: "greater", value: 0 },
        name: "refrigerator_type",
        id: 11
      },
      {
        text: "About how old is your most used refrigerator? Your best estimate is fine.",
        options: [
          "Less than 2 years old",
          "2 to 4 years old",
          "5 to 9 years old",
          "10 to 14 years old",
          "15 to 19 years old",
          "20 or more years old",
          "Don't know"
        ],
        condition: { questionId: 9, operator: "greater", value: 0 },
        name: "refrigerator_age",
        id: 12
      },
      {
        text: "How many stoves/ranges do you have in your home? A stove has both a cooktop and an oven.If none, please enter \"0.\"",
        input: "number",
        placeholder: "Number of stoves/ranges",
        min: "0",
        step: "1",
        name: "num_stoves",
        id: 13 // Dependent question for 'stove_fuel'
      },
      {
        text: "What fuel does your most used stove/range use?",
        options: [
          "Electricity",
          "Natural gas from underground pipes",
          "Propane (bottled gas)",
          "Liquid petroleum gas (LPG)",
          "Other (please specify)"
        ],
        hasOther: true,
        condition: { questionId: 13, operator: "greater", value: 0 },
        name: "stove_fuel",
        id: 14
      },
      {
        text: "How many separate wall ovens do you have in your home? Do not include wall ovens that are attached to a cooktop.If none, please enter \"0.\"",
        input: "number",
        placeholder: "Number of separate wall ovens",
        min: "0",
        step: "1",
        name: "num_wall_ovens",
        id: 15 // Dependent question for 'wall_oven_fuel', 'wall_oven_usage'
      },
      {
        text: "What fuel does your most used separate wall oven use?",
        options: [
          "Electricity",
          "Natural gas from underground pipes",
          "Propane (bottled gas)",
          "Other (please specify)"
        ],
        hasOther: true,
        condition: { questionId: 15, operator: "greater", value: 0 },
        name: "wall_oven_fuel",
        id: 16
      },
      {
        text: "In a typical week, about how many times is your most used separate wall oven used? If not used, please enter \"0.\"",
        input: "number",
        placeholder: "Times per week",
        min: "0",
        step: "1",
        condition: { questionId: 15, operator: "greater", value: 0 },
        name: "wall_oven_usage",
        id: 17
      },
      {
        text: "Are any of the following small kitchen appliances used at least once a week in your home?",
        type: "yes_no_grid",
        appliances: [
          "Toaster",
          "Toaster oven",
          "Coffee maker",
          "Crock pot or slow cooker",
          "Food processor",
          "Rice cooker",
          "Blender or juicer",
          "Other (please specify)"
        ],
        id: 18
      },

      // Laundry Appliances
      {
        text: " Does your household have a clothes washer? Do not include community clothes washers that are located in the basement or laundry room of your apartment building.",
        options: ["Yes", "No"],
        name: "has_clothes_washer",
        id: 19 // Dependent question for 'clothes_washer_usage', 'clothes_washer_age'
      },
      {
        text : " In a typical week, about how many times is your clothes washer used? If not used, please enter \"0.\"",
        input: "number",
        placeholder: "Times per week",
        min: "0",
        step: "1",
        condition: { questionId: 19, value: "Yes" },
        name: "clothes_washer_usage",
        id: 20
      },
      {
        text: "About how old is your clothes washer? Your best estimate is fine. ",
        options: [
          "Less than 2 years old",
          "2 to 4 years old",
          "5 to 9 years old",
          "10 to 14 years old",
          "15 to 19 years old",
          "20 or more years old",
          "Don't know"
        ],
        condition: { questionId: 19, value: "Yes" },
        name: "clothes_washer_age",
        id: 21
      },
      {
        text: "Does your household have a clothes dryer?",
        options: ["Yes", "No"],
        name: "has_clothes_dryer",
        id: 22 // Dependent question for 'uses_clothes_dryer_type', 'clothes_dryer_fuel', 'clothes_dryer_age'
      },
      {
        text: "What type of clothes dryer do you have?",
        options: [
            "Vented electric dryer",
            "Ventless electric dryer",
            "Gas dryer"
        ],
        condition: { questionId: 22, value: "Yes" },
        name: "uses_clothes_dryer_type",
        id: 23
      },
      {
        text: "What fuel does your clothes dryer use?",
        options: [
          "Electricity",
          "Natural gas from underground pipes",
          "Propane (bottled gas)",
          "Other (please specify)"
        ],
        hasOther: true,
        condition: { questionId: 22, value: "Yes" },
        name: "clothes_dryer_fuel",
        id: 24
      },
      {
        text: "About how old is your clothes dryer? Your best estimate is fine.",
        options: [
          "Less than 2 years old",
          "2 to 4 years old",
          "5 to 9 years old",
          "10 to 14 years old",
          "15 to 19 years old",
          "20 or more years old",
          "Don't know"
        ],
        condition: { questionId: 22, value: "Yes" },
        name: "clothes_dryer_age",
        id: 25
      },

      // Electronics & Internet Usage
      {
        text: " How many televisions are used in your home? If none, please enter \"0.\" ",
        input: "number",
        placeholder: "Number of televisions",
        min: "0",
        step: "1",
        name: "num_televisions",
        id: 26 // Dependent question for 'tv_size', 'tv_type', 'tv_daily_hours'
      },
      {
        text: "What is the size of your most used television?",
        options: [
          "Less than 27 inches",
          "27 to 39 inches",
          "40 to 59 inches",
          "60 inches or larger"
        ],
        condition: { questionId: 26, operator: "greater", value: 0 },
        name: "tv_size",
        id: 27
      },
      {
        text: "What type of television do you have?",
        options: [
          "CRT (cathode ray tube)",
          "LCD (liquid crystal display)",
          "LED (light-emitting diode)",
          "Plasma",
          "OLED (organic light-emitting diode)",
          "Other (please specify)"
        ],hasOther: true,
        condition: { questionId: 26, operator: "greater", value: 0 },
        name: "tv_type",
        id: 28
      },
      {
        text : " Thinking about your most used television's use on weekdays, how many hours is it turned on each day? Include the time it is on even if no one is actually watching it. ",
        input : "number",
        placeholder : "Hours per day",
        min: "0",
        step: "1",
        condition: { questionId: 26, operator: "greater", value: 0 },
        name: "tv_daily_hours",
        id: 29
      },
      {
        text: "How many of each of the following are used in your home? If none, please enter \"0.\"",
        type: "multiple_number",
        devices: [
          { label: "Number of desktop computers", name: "num_desktop_computers" },
          { label: "Number of laptop computers", name: "num_laptop_computers" },
          { label: "Number of tablet computers or e-readers (for example: iPad or Kindle)", name: "num_tablets_ereaders" },
          { label: "Number of printers, scanners, fax machines, or copiers", name: "num_printers_scanners_etc" },
          { label: "Number of \"smart\" phones (for example, iPhone or Android)", name: "num_smart_phones" },
          { label: "Number of other cellular phones", name: "num_other_cell_phones" }
        ],
        id: 30
      },
      {
        text: "In your home, do you or any members of your household access the Internet? ",
        options: ["Yes", "No"],
        name: "access_internet",
        id: 31 // Dependent question for 'has_wireless_router'
      },
      {
        text: " Is a wireless router used in your home for accessing the Internet?",
        options: ["Yes", "No", "Don't know"],
        condition: { questionId: 31, value: "Yes" },
        name: "has_wireless_router",
        id: 32
      },

      // Space Heating
      {
        text: "Is your home heated during the winter?",
        options: ["Yes", "No, I do not have any heating equipment.", " No, I have heating equipment but do not use it."],
        name: "is_home_heated",
        id: 33 // Dependent question for 'main_heating_equipment', 'main_heating_equipment_age', 'main_heating_fuel'
      },
      {
        text: " What is the main type of heating equipment used to provide heat for your home?",
        options: [
          "Central furnace",
          "Heat pump",
          "Steam or hot water system with radiators or pipes",
          "Built-in electric units installed in walls, ceilings, baseboards, or floors",
          "Built-in floor/wall pipeless furnace",
          "Built-in room heater burning gas, oil, or kerosene",
          "Heating stove burning wood, coal, or coke",
          "Portable electric heaters",
          "Other (please specify)"
        ],
        hasOther: true,
        condition: { questionId: 33, value: "Yes" },
        name: "main_heating_equipment",
        id: 34
      },
      {
        text: "About how old is your main heating equipment? Your best estimate is fine. ",
        options: [
          "Less than 2 years old",
          "2 to 4 years old",
          "5 to 9 years old",
          "10 to 14 years old",
          "15 to 19 years old",
          "20 or more years old",
          "Don't know"
        ],
        condition: { questionId: 33, value: "Yes" },
        name: "main_heating_equipment_age",
        id: 35
      },
      {
        text:"What is the main fuel used by this equipment for heating your home?",
        options: [
          "Electricity",
          "Natural gas from underground pipes",
          "Propane (bottled gas)",
          "Fuel oil or kerosene",
          "Wood",
          "Other (please specify)"
        ],
        hasOther: true,
        condition: { questionId: 33, value: "Yes" },
        name: "main_heating_fuel",
        id: 36
      },

      // Air Conditioning & Cooling
      {
        text: "Is any air conditioning equipment used in your home? ",
        options: ["Yes", "No"],
        name: "has_ac",
        id: 37 // Dependent question for 'uses_central_ac' and 'temp_summer_day_home' (input_group)
      },
      {
        text: " Do you use a central air conditioning system?",
        options: ["Yes", "No"],
        condition: { questionId: 37, value: "Yes" },
        name: "uses_central_ac",
        id: 38 // Dependent question for 'central_ac_is_heat_pump', 'central_ac_age'
      },
      {
        text : " Is your central air conditioning system a heat pump? ",
        options: ["Yes", "No", "Don't know"],
        condition: { questionId: 38, value: "Yes" },
        name: "central_ac_is_heat_pump",
        id: 39
      },
      {
        text : "About how old is your central air conditioning system? Your best estimate is fine. ",
        options: [
          "Less than 2 years old",
          "2 to 4 years old",
          "5 to 9 years old",
          "10 to 14 years old",
          "15 to 19 years old",
          "20 or more years old",
          "Don't know"
        ],
        condition: { questionId: 38, value: "Yes" },
        name: "central_ac_age",
        id: 40
      },
      {
        text: "The next questions are about the temperature inside your home during the summer. If you have a thermostat, think about where your household sets the temperature for your air conditioning equipment. If you do not have a thermostat, your best guess about the temperature is fine. ",
        type: "input_group",
        section: [
          {
            title: " During the summer, what is the typical temperature when someone is home during the day? ",
            inputType: "number",
            placeholder: "degrees",
            min: -273.15,
            step: "0.01",
            name: "temp_summer_day_home"
          },
          {
            title: " What is the typical temperature when no one is inside your home during the day? ",
            inputType: "number",
            placeholder: "degrees",
            min: -273.15,
            step: "0.01",
            name: "temp_summer_day_away"
          },
          {
            title: " What is the typical temperature inside your home at night? ",
            inputType: "number",
            placeholder: "degrees",
            min: -273.15,
            step: "0.01",
            name: "temp_summer_night"
          }
        ],
        condition: { questionId: 37, value: "Yes" },
        id: 41
      },
      {
        text: "How many of the following types of fans does your household use? If none, please enter “0.”",
        type: "multiple_number",
        devices: [
          { label: "Number of ceiling fans", name: "num_ceiling_fans" },
          { label: "Number of floor or window fans", name: "num_floor_window_fans" },
          { label: "Number of whole house fans", name: "num_whole_house_fans" },
          { label: "Number of attic fans", name: "num_attic_fans" }
        ],
        id: 42
      },

      // Water Heating
      {
        text: "Does your home have a water heater?",
        options: ["Yes", "No"],
        name: "has_water_heater",
        id: 43 // Dependent question for 'water_heater_size', 'water_heater_age', 'water_heater_fuel'
      },
      {
        text: " What is the approximate size of your main water heater? ",
        options: [
            "Small (less than 15 litres)",
            "Medium (15 to 25 litres)",
            "Large (more than 25 litres)",
            "Tankless (instant/on-demand)",
            "Don't know"
        ],
        condition: { questionId: 43, value: "Yes" },
        name: "water_heater_size",
        id: 44
      },
      {
        text: "About how old is your main water heater? Your best estimate is fine. ",
        options: [
          "Less than 2 years old",
          "2 to 4 years old",
          "5 to 9 years old",
          "10 to 14 years old",
          "15 to 19 years old",
          "20 or more years old",
          "Don't know"
        ],
        condition: { questionId: 43, value: "Yes" },
        name: "water_heater_age",
        id: 45
      },
      {
        text: "What fuel does your main water heater use?",
        options: [
          "Electricity",
          "Natural gas from underground pipes",
          "Propane (bottled gas)",
          "Fuel oil or kerosene",
          "Solar",
          "Don't know",
          "Other (please specify)"
        ],hasOther: true,
        condition: { questionId: 43, value: "Yes" },
        name: "water_heater_fuel",
        id: 46
      },

      // Lighting
      {
        text: " Approximately how many light bulbs are installed inside your home? Include light bulbs in ceiling fixtures and fans, table and floor lamps, as well as those used infrequently, such as in hallways, closets, and garages. For fixtures with multiple bulbs, count each bulb separately. ",
        options: [
          "Less than 10",
          "10 to 19",
          "20 to 29",
          "30 to 39",
          "40 to 49",
          "50 or more",
          "Don't know"
        ],
        name: "num_light_bulbs_total",
        id: 47
      },
      {
        text: " How many of the light bulbs inside your home are used at least 4 hours per day? ",
        input: "number",
        placeholder: "Light bulbs",
        min: "0",
        step: "1",
        name: "num_light_bulbs_4hr_plus",
        id: 48
      },
      {
        text: " Are any of the following types of light bulbs used outside your home? ",
        type: "yes_no_grid",
        appliances: [
          "Incandescent",
          "Natural gas lights",
          "CFL (compact fluorescent lamp)",
          "LED (light-emitting diode)"
        ],
        id: 49
      },

      // Energy Payment & Generation
      {
        text:"Which of the following describes who is responsible for paying for the electricity used in this home?",
        options: [
          "Household is responsible for paying for all electricity used in this home",
          "All electricity used in this home is included in the rent or condo fee",
          "Some is paid by the household, some is included in the rent or condo fee",
          "Don't know",
          "Other (please specify)"
        ], hasOther: true,
        name: "electricity_payment_responsibility",
        id: 50
      },
      {
        text: "Which of the following describes who is responsible for paying for the natural gas used in this home?",
        options: [
          "Household is responsible for paying for all natural gas used in this home",
          "All natural gas used in this home is included in the rent or condo fee",
          "Some is paid by the household, some is included in the rent or condo fee",
          "Don't know",
          "Other (please specify)"
        ], hasOther: true,
        name: "natural_gas_payment_responsibility",
        id: 51
      },
      {
        text: "Which of the following describes who is responsible for paying for the fuel oil used in this home?",
        options: [
          "Household is responsible for paying for all fuel oil used in this home",
          "All fuel oil used in this home is included in the rent or condo fee",
          "Some is paid by the household, some is included in the rent or condo fee",
          "Don't know",
          "Other (please specify)"
        ], hasOther: true,
        name: "fuel_oil_payment_responsibility",
        id: 52
      },
      {
        text: "Does your household have a back-up generator that can be used for generating electricity in case of a power outage or emergency?",
        options: ["Yes", "No"],
        name: "has_backup_generator",
        id: 53
      },
      {
        text: "Not including back-up generators, does your home have any of these on-site systems that generate electricity? Please select all that apply.",
        options: [
          "No on-site generation system",
          "Solar or photovoltaic system",
          "Small wind turbine",
          "Combined heat and power system",
          "Other (please specify)"
        ], hasOther: true,
        name: "on_site_electricity_generation",
        id: 54
      },
      {
        text: "What is your average annual household spending on electricity?",
        options: [
          "Less than ₹50,000",
          "₹50,000 to ₹1,00,000",
          "₹1,00,001 to ₹1,50,000",
          "₹1,50,001 to ₹2,00,000",
          "More than ₹2,00,000",
          "Prefer not to answer"
        ],
        name: "avg_annual_electricity_spending",
        id: 55
      },
      {
        text: "Does your household receive fuel oil or kerosene deliveries?",
        options: ["Yes", "No"],
        name: "receives_fuel_oil_deliveries",
        id: 56 // Dependent question for 'fuel_oil_tank_size' (input_group)
      },
      {
        text: "Please provide as much of the following information as you can about your fuel oil or kerosene deliveries:",
        type: "input_group",
        section: [
          {
            title: "tank size",
            inputType: "number",
            placeholder: "liters",
            min: "0",
            step: "any",
            name: "fuel_oil_tank_size"
          },
          {
            title: "Number of fuel oil or kerosene deliveries in the past year:",
            inputType: "number",
            placeholder: "Number of deliveries",
            min: "0",
            step: "1",
            name: "fuel_oil_num_deliveries_past_year"
          },
          // Removed: {
          //   title: "Total liters of fuel oil or kerosene used in the past year:",
          //   inputType: "number",
          //   placeholder: "Total liters",
          //   min: "0",
          //   step: "any",
          //   name: "fuel_oil_total_gallons_past_year"
          // },
          {
            title: "Total cost of fuel oil or kerosene used in the past year:",
            inputType: "number",
            placeholder: "Total cost in rupees",
            min: "0",
            step: "any",
            name: "fuel_oil_total_cost_past_year"
          }
        ],
        condition: { questionId: 56, value: "Yes" },
        name: "fuel_use_details", // Added a name for the input group question itself
        id: 57
      },
      {
        text: "does your household use wood for fuel?",
        options: ["Yes", "No"],
        name: "uses_wood_for_fuel",
        id: 58 // Dependent question for 'wood_pellets_total_amount_past_year' (input_group)
      },
      {
        text: "Please provide as much of the following information as you can about your wood use:",
        type: "input_group",
        section: [
          {
            title: "Total amount of wood pellets used in the past year:",
            inputType: "number",
            placeholder: "tons",
            min: "0",
            step: "any",
            name: "wood_pellets_total_amount_past_year"
          },
          {
            title: "Total cost of wood used in the past year:",
            inputType: "number",
            placeholder: "Cost in rupees",
            min: "0",
            step: "any",
            name: "wood_total_cost_past_year"
          }
        ],
        condition: { questionId: 58, value: "Yes" },
        name: "wood_use_details", // Added a name for the input group question itself
        id: 59
      },
      // NEW QUESTION - LPG/Propane Cylinders
      {
        text: "How many LPG or propane cylinders does your household use in a year?",
        input: "number",
        placeholder: "Number of cylinders",
        min: "0",
        step: "1",
        name: "num_lpg_propane_cylinders_year",
        id: 60
      },
      {
        text: "what is the last electricity bill amount you paid?",
        input: "number",
        placeholder: "Electricity bill amount in rupees",
        min: "0",
        step: "any",
        name: "last_electricity_bill_amount",
        id: 61
      },
      {
        text: "How much electricity did you consume the last time you paid the bill?",
        input: "number",
        placeholder: "Electricity consumption in kWh",
        min: "0",
        step: "any",
        name: "last_electricity_consumption",
        id: 62
      }
    ];

    const questionsDiv = document.getElementById("questions");
    const surveyForm = document.getElementById("surveyForm");
    const resetBtn = document.getElementById("resetBtn");
    const statusDiv = document.getElementById("status");

    // Function to render all questions
    function renderAllQuestions() {
        questionsDiv.innerHTML = ""; // Clear existing content

        questions.forEach(q => {
            const block = document.createElement("div");
            block.className = "question-block";
            block.setAttribute("data-question-id", q.id); // For conditional visibility

            const questionText = document.createElement("div");
            questionText.className = "question-text";
            questionText.textContent = q.text;
            block.appendChild(questionText);

            let inputHtml = '';

            if (q.input === "number" || q.input === "text") {
                inputHtml = `<input type="${q.input}" name="Q${q.id}_${q.name}" placeholder="${q.placeholder || ''}" ${q.min !== undefined ? `min="${q.min}"` : ''} ${q.step !== undefined ? `step="${q.step}"` : ''} required>`;
                block.innerHTML += inputHtml;
            } else if (q.input === "multiple") {
                let multipleInputHtml = '';
                q.inputs.forEach(inputDef => {
                    const inputName = `Q${q.id}_${inputDef.name}`;
                    multipleInputHtml += `
                        <div class="input-group-item">
                            <label for="${inputName}">${inputDef.placeholder}:</label>
                            <input type="${inputDef.type}" id="${inputName}" name="${inputName}" placeholder="${inputDef.placeholder}" ${inputDef.pattern ? `pattern="${inputDef.pattern}"` : ''} required />
                        </div>
                    `;
                });
                block.innerHTML += multipleInputHtml;
            } else if (q.type === "checkbox") { // This is for the sq_ft_basement/attic/garage, which are radio groups
                q.sections.forEach(section => {
                    const sectionDiv = document.createElement("div");
                    sectionDiv.className = "section";
                    sectionDiv.innerHTML = `<h4>${section.title}</h4>`;
                    section.options.forEach(opt => {
                        sectionDiv.innerHTML += `
                            <label>
                                <input type="radio" name="Q${q.id}_${section.name}" value="${opt}" />
                                ${opt}
                            </label>
                        `;
                    });
                    block.appendChild(sectionDiv);
                });
            } else if (q.type === "yes_no_grid") {
                const gridDiv = document.createElement("div");
                gridDiv.className = "yes-no-grid";

                const headerDiv = document.createElement("div");
                headerDiv.className = "grid-header";
                headerDiv.innerHTML = `
                    <div class="appliance-label">Appliance</div>
                    <div class="yes-no-options">
                        <span>Yes</span>
                        <span>No</span>
                    </div>
                `;
                gridDiv.appendChild(headerDiv);

                q.appliances.forEach((appliance, index) => {
                    const rowDiv = document.createElement("div");
                    rowDiv.className = "grid-row";

                    const applianceName = appliance.replace(/[^a-zA-Z0-9]/g, '_');
                    rowDiv.innerHTML = `
                        <div class="appliance-name">${String.fromCharCode(65 + index)}. ${appliance}</div>
                        <div class="yes-no-buttons">
                            <label><input type="radio" name="Q${q.id}_${applianceName}" value="Yes" /><span class="radio-custom"></span></label>
                            <label><input type="radio" name="Q${q.id}_${applianceName}" value="No" /><span class="radio-custom"></span></label>
                        </div>
                    `;
                    gridDiv.appendChild(rowDiv);

                    if (appliance.includes("Other (please specify)")) {
                        const otherDiv = document.createElement("div");
                        otherDiv.className = "other-input-grid";
                        otherDiv.innerHTML = `<input type="text" name="Q${q.id}_${applianceName}_other" placeholder="Please specify..." style="width: calc(100% - 40px);" disabled />`;
                        gridDiv.appendChild(otherDiv);
                    }
                });
                block.appendChild(gridDiv);
            } else if (q.type === "multiple_number") {
                const inputsDiv = document.createElement("div");
                inputsDiv.className = "multiple-number-inputs";
                q.devices.forEach((device, index) => {
                    inputsDiv.innerHTML += `
                        <div class="number-input-row">
                            <div class="device-label">${device.label}</div>
                            <input type="number" name="Q${q.id}_${device.name}" min="0" step="1" required />
                        </div>
                    `;
                });
                block.appendChild(inputsDiv);
            } else if (q.type === "input_group") {
                q.section.forEach(inputSection => {
                    const inputDiv = document.createElement("div");
                    inputDiv.className = "input-section";
                    inputDiv.innerHTML = `<h4>${inputSection.title}</h4>`;
                    inputDiv.innerHTML += `
                        <input type="${inputSection.inputType}" name="Q${q.id}_${inputSection.name}"
                            placeholder="${inputSection.placeholder || ''}"
                            ${inputSection.min !== undefined ? `min="${inputSection.min}"` : ''}
                            ${inputSection.step !== undefined ? `step="${inputSection.step}"` : ''}
                            ${inputSection.pattern ? `pattern="${inputSection.pattern}"` : ''}
                            required />
                    `;
                    block.appendChild(inputDiv);
                });
            } else {
                // Regular radio button questions
                q.options.forEach(opt => {
                    block.innerHTML += `
                        <label>
                            <input type="radio" name="Q${q.id}_${q.name}" value="${opt}" />
                            ${opt}
                        </label>
                    `;
                });
                if (q.hasOther) {
                    block.innerHTML += `<div class="other-input"><input type="text" name="Q${q.id}_other" placeholder="Please specify..." style="width: calc(100% - 40px);" disabled /></div>`;
                }
            }

            questionsDiv.appendChild(block);
        });
        updateQuestionVisibility(); // Set initial visibility based on conditions
    }

    // Function to collect all form data with defaults for hidden fields
    function collectFormData() {
        const formData = {};
        const formElements = surveyForm.elements;
        const currentAnswers = {}; // To store answers of currently visible/enabled fields

        // First pass: Collect data from all *enabled* elements
        for (let i = 0; i < formElements.length; i++) {
            const element = formElements[i];
            if (element.name && !element.disabled) {
                if (element.type === "radio") {
                    if (element.checked) {
                        currentAnswers[element.name] = element.value;
                    }
                } else if (element.type === "checkbox") {
                    if (element.checked) {
                        currentAnswers[element.name] = element.value;
                    }
                } else if (element.tagName === "INPUT" || element.tagName === "TEXTAREA" || element.tagName === "SELECT") {
                    currentAnswers[element.name] = element.value;
                }
            }
        }

        // Second pass: Iterate through all defined questions and assign values/defaults
        questions.forEach(q => {
            const questionBlock = document.querySelector(`[data-question-id="${q.id}"]`);
            let isQuestionVisible = true; // Assume visible unless hidden by condition

            // Re-evaluate visibility based on current answers to determine if it *should* be visible
            if (q.condition) {
                const conditionQuestionDef = questions.find(item => item.id === q.condition.questionId);
                let conditionInputName;
                if (conditionQuestionDef) {
                    if (conditionQuestionDef.input === "number" || conditionQuestionDef.input === "text") {
                        conditionInputName = `Q${conditionQuestionDef.id}_${conditionQuestionDef.name}`;
                    } else if (conditionQuestionDef.input === "multiple") {
                        conditionInputName = `Q${conditionQuestionDef.id}_${conditionQuestionDef.inputs[0].name}`;
                    } else { // For select/radio type questions, it's just their main name
                        conditionInputName = `Q${conditionQuestionDef.id}_${conditionQuestionDef.name}`;
                    }
                }

                // Get the answer for the conditional question. If not found, default to an empty string for evaluation.
                const answerForCondition = currentAnswers[conditionInputName] || '';

                if (q.condition.operator === "greater") {
                    isQuestionVisible = parseFloat(answerForCondition) > q.condition.value;
                } else {
                    isQuestionVisible = answerForCondition === q.condition.value;
                }
            }

            // Assign values or defaults based on visibility and type
            if (q.input === "text" || q.input === "number") {
                const name = `Q${q.id}_${q.name}`;
                if (isQuestionVisible && currentAnswers[name] !== undefined && currentAnswers[name] !== '') {
                    formData[name] = q.input === "number" ? parseFloat(currentAnswers[name]) : currentAnswers[name];
                } else {
                    formData[name] = q.input === "number" ? 0 : "";
                }
            } else if (q.input === "multiple") { // For city/pincode
                q.inputs.forEach(inputDef => {
                    const name = `Q${q.id}_${inputDef.name}`;
                    if (isQuestionVisible && currentAnswers[name] !== undefined && currentAnswers[name] !== '') {
                        formData[name] = currentAnswers[name];
                    } else {
                        formData[name] = "";
                    }
                });
            } else if (q.type === "checkbox") { // For sq_ft_basement/attic/garage (radio groups)
                q.sections.forEach(section => {
                    const name = `Q${q.id}_${section.name}`;
                    if (isQuestionVisible && currentAnswers[name] !== undefined) {
                        formData[name] = currentAnswers[name];
                    } else {
                        formData[name] = "Not applicable (my home does not have this space)";
                    }
                });
            } else if (q.type === "yes_no_grid") {
                q.appliances.forEach(appliance => {
                    const applianceName = appliance.replace(/[^a-zA-Z0-9]/g, '_');
                    const name = `Q${q.id}_${applianceName}`;
                    if (isQuestionVisible && currentAnswers[name] !== undefined) {
                        formData[name] = currentAnswers[name];
                    } else {
                        formData[name] = "No";
                    }

                    if (appliance.includes("Other (please specify)")) {
                        const otherName = `Q${q.id}_${applianceName}_other`;
                        if (isQuestionVisible && currentAnswers[otherName] !== undefined && currentAnswers[otherName] !== '') {
                            formData[otherName] = currentAnswers[otherName];
                        } else {
                            formData[otherName] = "";
                        }
                    }
                });
            } else if (q.type === "multiple_number") {
                q.devices.forEach(device => {
                    const name = `Q${q.id}_${device.name}`;
                    if (isQuestionVisible && currentAnswers[name] !== undefined && currentAnswers[name] !== '') {
                        formData[name] = parseFloat(currentAnswers[name]);
                    } else {
                        formData[name] = 0;
                    }
                });
            } else if (q.type === "input_group") {
                q.section.forEach(inputSection => {
                    const name = `Q${q.id}_${inputSection.name}`;
                    if (isQuestionVisible && currentAnswers[name] !== undefined && currentAnswers[name] !== '') {
                        formData[name] = parseFloat(currentAnswers[name]);
                    } else {
                        formData[name] = 0;
                    }
                });
            } else { // Standard radio button questions (options)
                const name = `Q${q.id}_${q.name}`;
                if (isQuestionVisible && currentAnswers[name] !== undefined) {
                    formData[name] = currentAnswers[name];
                } else {
                    formData[name] = "";
                }
                if (q.hasOther) {
                    const otherName = `Q${q.id}_other`;
                    if (isQuestionVisible && currentAnswers[otherName] !== undefined && currentAnswers[otherName] !== '') {
                        formData[otherName] = currentAnswers[otherName];
                    } else {
                        formData[otherName] = "";
                    }
                }
            }
        });

        for (let i = 0; i < formElements.length; i++) {
            const element = formElements[i];
            if (element.name && !element.disabled && formData[element.name] === undefined) {
                if (element.type === "radio") {
                    if (element.checked) {
                        formData[element.name] = element.value;
                    }
                } else if (element.type === "checkbox") {
                    if (element.checked) {
                        formData[element.name] = element.value;
                    }
                } else {
                    formData[element.name] = element.value;
                }
            }
        }
        return formData;
    }

    // Function to update visibility of conditional questions and 'other' inputs
    function updateQuestionVisibility() {
      const currentAnswers = {}; // Get current state of answers from *all* fields
      const formElements = surveyForm.elements;
      for (let i = 0; i < formElements.length; i++) {
          const element = formElements[i];
          if (element.name) {
              if (element.type === "radio") {
                  if (element.checked) {
                      currentAnswers[element.name] = element.value;
                  }
              } else if (element.type === "checkbox") {
                  if (element.checked) {
                      currentAnswers[element.name] = element.value;
                  }
              } else if (element.tagName === "INPUT" || element.tagName === "TEXTAREA" || element.tagName === "SELECT") {
                  currentAnswers[element.name] = element.value;
              }
          }
      }

      questions.forEach(q => {
        const questionBlock = document.querySelector(`[data-question-id="${q.id}"]`);
        if (!questionBlock) return;

        let shouldBeVisible = true; // Default to visible

        // Handle conditional question visibility
        if (q.condition) {
          const conditionQuestionId = q.condition.questionId;
          const conditionValue = q.condition.value;
          const conditionOperator = q.condition.operator;

          const conditionQuestionDef = questions.find(item => item.id === conditionQuestionId);

          let conditionInputName;
          if (conditionQuestionDef) {
            if (conditionQuestionDef.input === "number" || conditionQuestionDef.input === "text") {
              conditionInputName = `Q${conditionQuestionDef.id}_${conditionQuestionDef.name}`;
            } else if (conditionQuestionDef.input === "multiple") {
                conditionInputName = `Q${conditionQuestionDef.id}_${conditionQuestionDef.inputs[0].name}`; // Use the first input's name for multiple
            } else {
              conditionInputName = `Q${conditionQuestionDef.id}_${conditionQuestionDef.name}`;
            }
          }

          // Get the answer for the conditional question. If not found, assume default 'No' or 0 for checks.
          // This prevents hidden fields from breaking visibility logic.
          let answerForCondition = currentAnswers[conditionInputName];
          if (answerForCondition === undefined) {
              // Provide a default based on expected type if not answered/visible yet
              if (conditionQuestionDef && (conditionQuestionDef.input === 'number' || conditionQuestionDef.type === 'multiple_number' || conditionQuestionDef.type === 'input_group')) {
                  answerForCondition = 0; // Default numbers to 0
              } else {
                  answerForCondition = ''; // Default non-numbers to empty string
              }
          }


          if (conditionOperator === "greater") {
            shouldBeVisible = parseFloat(answerForCondition) > conditionValue;
          } else {
            shouldBeVisible = answerForCondition === conditionValue;
          }
        }

        if (shouldBeVisible) {
            questionBlock.style.display = 'block';
            questionBlock.querySelectorAll('input, select, textarea').forEach(input => {
                input.removeAttribute('disabled');
            });
        } else {
            questionBlock.style.display = 'none';
            questionBlock.querySelectorAll('input, select, textarea').forEach(input => {
                input.setAttribute('disabled', 'true');
                // Clear values of hidden fields to ensure clean submission
                if (input.type === 'radio' || input.type === 'checkbox') {
                    input.checked = false;
                } else {
                    input.value = '';
                }
            });
        }

        // Handle "Other (please specify)" input visibility
        if (q.hasOther) {
            const otherInput = questionBlock.querySelector(`input[name="Q${q.id}_other"]`);
            if (otherInput) {
                const selectedOption = questionBlock.querySelector(`input[name="Q${q.id}_${q.name}"]:checked`);
                if (selectedOption && selectedOption.value.includes("Other (please specify)")) {
                    otherInput.removeAttribute('disabled');
                    otherInput.setAttribute('required', 'true');
                } else {
                    otherInput.setAttribute('disabled', 'true');
                    otherInput.removeAttribute('required');
                    otherInput.value = '';
                }
            }
        }
        // Handle "Other (please specify)" for yes_no_grid
        if (q.type === "yes_no_grid") {
            q.appliances.forEach(appliance => {
                if (appliance.includes("Other (please specify)")) {
                    const applianceName = appliance.replace(/[^a-zA-Z0-9]/g, '_');
                    const yesRadio = questionBlock.querySelector(`input[name="Q${q.id}_${applianceName}"][value="Yes"]`);
                    const otherInput = questionBlock.querySelector(`input[name="Q${q.id}_${applianceName}_other"]`);

                    if (yesRadio && otherInput) {
                        // The 'other' input should be enabled if 'Yes' is selected for "Other (please specify)"
                        if (yesRadio.checked) {
                            otherInput.removeAttribute('disabled');
                            otherInput.setAttribute('required', 'true');
                        } else {
                            otherInput.setAttribute('disabled', 'true');
                            otherInput.removeAttribute('required');
                            otherInput.value = '';
                        }
                    }
                }
            });
        }
      });
    }

    // Add event listeners to all relevant inputs for real-time visibility updates
    // Use a delegated event listener on questionsDiv for efficiency
    questionsDiv.addEventListener('change', (event) => {
        // Only trigger update if the changed element is an input within a question block
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'SELECT' || event.target.tagName === 'TEXTAREA') {
            updateQuestionVisibility();
        }
    });


    // Event listener for Reset button
    resetBtn.addEventListener("click", () => {
      surveyForm.reset(); // Resets all form fields
      updateQuestionVisibility(); // Reset visibility for conditional questions
      statusDiv.textContent = ""; // Clear status message
      statusDiv.style.color = ""; // Reset status color
    });

    // Event listener for form submission
    surveyForm.addEventListener("submit", async function (event) {
      event.preventDefault(); // Prevent default form submission

      statusDiv.textContent = ""; // Clear previous status messages
      statusDiv.style.color = ""; // Reset color

      // Client-side validation for all currently visible fields
      const allInputs = surveyForm.querySelectorAll('input:not([disabled]), select:not([disabled]), textarea:not([disabled])');
      let formIsValid = true;
      let firstInvalidElement = null;

      allInputs.forEach(input => {
        // Clear previous error messages for this input
        const existingError = input.nextElementSibling;
        if (existingError && existingError.classList.contains('error-message')) {
          existingError.remove();
        }

        // Specific validation for number types
        if (input.type === 'number') {
            const numVal = parseFloat(input.value);
            if (isNaN(numVal) && input.hasAttribute('required') && input.value.trim() === "") {
                formIsValid = false;
                if (!firstInvalidElement) firstInvalidElement = input;
                displayError(input, 'Please enter a number.');
            } else if (input.min && numVal < parseFloat(input.min)) {
                formIsValid = false;
                if (!firstInvalidElement) firstInvalidElement = input;
                displayError(input, `Value must be at least ${input.min}.`);
            } else if (input.step && input.step !== "any") { // Improved step validation
                const step = parseFloat(input.step);
                // To avoid floating point issues, scale to integers for modulo check
                const precision = (step.toString().split('.')[1] || '').length;
                if (Math.abs((numVal * (10**precision)) % (step * (10**precision))) > 1e-9) { // Using a small epsilon
                    formIsValid = false;
                    if (!firstInvalidElement) firstInvalidElement = input;
                    displayError(input, `Value must be a multiple of ${input.step}.`);
                }
            }
        }
        // Specific validation for text inputs with patterns (e.g., pincode)
        else if (input.type === 'text' && input.pattern) {
          const regex = new RegExp(input.pattern);
          if (input.value.trim() === "" && input.hasAttribute('required')) {
            formIsValid = false;
            if (!firstInvalidElement) firstInvalidElement = input;
            displayError(input, 'This field is required.');
          } else if (!regex.test(input.value)) {
            formIsValid = false;
            if (!firstInvalidElement) firstInvalidElement = input;
            // Find the original question definition to get specific validation message
            const questionIdMatch = input.name.match(/^Q(\d+)/); // Match only integer ID now
            if (questionIdMatch) {
                const questionDef = questions.find(q => q.id.toString() === questionIdMatch[1]);
                if (questionDef && questionDef.input === 'multiple') {
                    const inputDef = questionDef.inputs.find(i => `Q${questionDef.id}_${i.name}` === input.name);
                    displayError(input, inputDef.validationMessage || 'Invalid format.');
                } else {
                    displayError(input, 'Invalid format.');
                }
            } else {
                displayError(input, 'Invalid format.');
            }
          }
        }
        // General required validation for other types (radio, select, etc.)
        else if (input.hasAttribute('required') && input.value.trim() === "") {
            // For radio buttons, check if at least one in the group is checked
            if (input.type === 'radio') {
                const radioGroup = document.querySelectorAll(`input[name="${input.name}"]:checked`);
                if (radioGroup.length === 0) {
                    formIsValid = false;
                    if (!firstInvalidElement) firstInvalidElement = input;
                    // Prevent duplicate error messages for the same radio group
                    if (!input.closest('.question-block').querySelector('.error-message')) {
                      displayError(input.closest('.question-block'), 'Please select an option.', true);
                    }
                }
            } else {
              formIsValid = false;
              if (!firstInvalidElement) firstInvalidElement = input;
              displayError(input, 'This field is required.');
            }
        }
      });

      if (!formIsValid) {
        statusDiv.textContent = "Please correct the errors in the form.";
        statusDiv.style.color = "red";
        if (firstInvalidElement) {
            firstInvalidElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return; // Stop submission if validation fails
      }

      // If validation passes, proceed with submission
      statusDiv.textContent = "Submitting survey...";
      statusDiv.style.color = "blue";

      const formData = collectFormData(); // Now this function handles defaults for hidden fields
      console.log("Collected FormData:", formData);

      try {
        const response = await fetch("/api/submit-survey", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

       if (response.ok) {
          surveyContainer.style.display = 'none';
          thankYouMessage.style.display = 'block';
          window.scrollTo(0, 0);
        } else {
          const result = await response.json();
          statusDiv.textContent = `Error: ${result.error || "Unknown error"}`;
          statusDiv.style.color = "red";
        }
      } catch (error) {
        console.error("Network error or submission error:", error);
        statusDiv.textContent = "Network error or submission failed. Please try again.";
        statusDiv.style.color = "red";
      }
    });

    function displayError(element, message, afterElement = false) {
      const errorDiv = document.createElement('div');
      errorDiv.className = 'error-message';
      errorDiv.textContent = message;

      if (afterElement) {
        element.appendChild(errorDiv);
      } else {
        element.parentNode.insertBefore(errorDiv, element.nextSibling);
      }
    }

    renderAllQuestions();
});