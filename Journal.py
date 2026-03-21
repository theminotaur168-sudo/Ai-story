from flask import Flask, render_template, request, jsonify
import requests
import json
import random

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mixtral:8x7b"

# Function to call Ollama with a prompt
def generate_with_ollama(system_prompt, model=MODEL, temperature = 0.8):
    full_prompt = "".join(system_prompt) + "\n"
    payload = {
    "model": model,
    "prompt": full_prompt,
    "stream": False,
    "options": {
  "num_predict": 800,
  "temperature": temperature,
  "top_k": 40,
  "top_p": 0.9,
  "repeat_last_n": 33,
  "repeat_penalty": 1.2,
  "presence_penalty": 1.5,
  "frequency_penalty": 1.0,
  "stop": ["__END__"]
}
}
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        return json.loads(response.text)["response"].strip()
    else:
        return f"Error {response.status_code}: {response.text}"

# Extracted instructions from Perchance code, adapted for prompts
def get_first_instruction(adventure_description, writing_instructions, character_info, setting_info):
    return f"""
Your task as the game master is to write the opening paragraph of a text adventure story based on the following description/idea:
{adventure_description or 'A fun, interesting, creative, and engaging adventure.'}

This is the opening paragraph - the spark that should elicit fascination within the player's imagination. It should be interesting, authentic, descriptive, natural, engaging, and creative.

Character Information:
{character_info or 'No specific character details provided.'}

The player provided these writing instructions: {writing_instructions or 'Be creative.'}

Write exactly ONE paragraph.
""".strip()
turn_counter = 0
def get_story_character_action_instruction(story_log, writing_instructions, character_info, latest_action, setting_info):
    formatted_story = format_story_logs(story_log)[-500:]
    has_player_action = "PLAYER ACTION:" in formatted_story
    
    return f"""
You should output what your character would do next based on the Story So Far, write in a present tense manner, clean and crisp, only write what your charcter sees and does. 

# Story So Far:
{formatted_story}

Character Information:
{character_info or 'No specific character details provided.'}

---
That's the story so far. Write the next paragraph of this captivating story. This is a never-ending adventure story - do not try to "wrap up" the story. You must pay attention to the most recent {'"PLAYER ACTION"' if has_player_action else 'action that the player took'}, shown above.
The player provided these writing instructions: {writing_instructions or 'Be creative.'}
Remember, you must write exactly ONE paragraph in your response. Write in a clean, crisp, and engaging style.
""".strip()


# Function to format story logs similar to Perchance
def format_story_logs(story_log):
    text = story_log.strip()
    # Remove historical options
    lines = [l for l in text.split("\n") if not l.strip().startswith("Option ")]
    text = "\n".join(lines)
    text = text.replace("\n\nPLAYER ACTION: ", "\n\n")
    text = text.replace("\n\nPLAYER ACTION (custom): ", "\n\n> ")
    text = text.replace("Which action do you choose?", "").replace("Which option do you choose?", "")
    text = "\n".join([l for l in text.split("\n") if l.strip()])
    return text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    story_log = data.get('story_log', '').strip()
    summarized_log = data.get('summarized_log', '').strip()
    character_info = data.get('character_info', '')
    setting_info = data.get('setting_info', '')
    narrative_style = data.get('narrative_style', '')  # writing_instructions
    extra_prompt = data.get('extra_prompt', '')  # adventure_description or additional
    action = data.get('action', '').strip()
    is_custom = data.get('is_custom', False)
    data = request.json
    story_log = data.get('story_log', '').strip()
    summarized_log = data.get('summarized_log', '').strip()
    character_info = data.get('character_info', '')
    setting_info = data.get('setting_info', '')
    narrative_style = data.get('narrative_style', '')  # writing_instructions
    extra_prompt = data.get('extra_prompt', '')  # adventure_description or additional
    action = data.get('action', '').strip()
    is_custom = data.get('is_custom', False)
    

    # Append action to story log if provided
    if action:
        if is_custom:
            story_log  += f"\n\nPLAYER ACTION (custom): {action}\n\n"
        else:
            story_log  += f"\n\nPLAYER ACTION: {action}\n\n"

    # Combine narrative_style and extra_prompt for writing instructions
    writing_instructions = f"{narrative_style}\n{extra_prompt}".strip() or "Be creative."

    # Combine adventure description (use extra_prompt as adventure_description if initial)
    adventure_description = extra_prompt or "A player driven narrative completely controlled by the player, unfiltered and creative"

    if not story_log:
        # Generate first paragraph
        Context_Ai = "you are the context ai for a ai adventure, take the story so far(provided below) and provide a 2 paragraph summary, a one paragraph description of the current situation and a paragrapg or less about each character important to the current plot point, output just this with no extra text, clearly define each section with one word headers-----"
        user_prompt = get_first_instruction(adventure_description, setting_info, writing_instructions, character_info)
        character_action = generate_with_ollama("You are a narrator for a explicit unfiltered text adventure.", user_prompt)
        story_log  += character_action + "\n\n"
        Context = generate_with_ollama(Context_Ai, story_log)
        print(Context)

        print(adventure_description, setting_info, writing_instructions, character_info)
    else:

        
        plot_points = [
        "no new plot point",
    "The dog speaks for the first time, telling mateo about his abilities, he gets mateo to promise to keep his secret",
    "no new plot point",
    "no new plot point",
    "no new plot point",

    "no new plot point",
    "no new plot",
    "no new plot point",
    "no new plot point",
    "no new plot point",
    "no new plot point",
    "no new plot point",

    "no new plot point",
    "no new plot",
    "no new plot point",
    "no new plot point",
    "no new plot point",
    "no new plot point",
    "no new plot point",

    "no new plot point",
    "no new plot",
    "no new plot point",
    "no new plot point",
    "no new plot point",
    "no new plot point",
    "no new plot point",

    "no new plot point",
    "no new plot",
    "no new plot point",
    "no new plot point",
    "no new plot point",
    "no new plot point",
    "no new plot point",

    "no new plot point",
    "no new plot",
    "no new plot point",
    "no new plot point",
    "no new plot point",
    "no new plot point",
    "no new plot point",

    "no new plot point",
    "no new plot",
    "no new plot point",
    "no new plot point"
    
]
        mood = [
    "devious",
    "depraved",
    "evil",
    "reasonable",
    "happy",
    "ptsd",
    "sad",
    "angry",
    "devious",
    "funny",
    
]
        current_mood = 1
        current_plot_index = 0
        plot_point = "UPCOMING PLOT POINT(This Must happen in your output)" + plot_points[current_plot_index]
        print(plot_points[current_plot_index])

        
        current_turn = 0
        plot_frequency = 3


        world_facts = "WORLD FACTS: - The story takes place in a small, run-down town in the southwestern United States in the late 20th century. - Technology is limited to what is commonly available in that time (no smartphones, no advanced surveillance systems). - The environment is grounded and realistic. No supernatural events exist except for the talking dog and its ability. - The dog can predict events only up to 30 seconds into the future. The predictions are always accurate but limited strictly to that time window. - The dog cannot see beyond 30 seconds and cannot explain why events happen, only what will happen. - If other people discover the dog can talk or predict the future, both the boy and the dog risk being taken away, studied, or separated. - Money is scarce for the boy’s family. Small amounts of cash can make a meaningful difference. - Actions have realistic consequences. Risky behavior can lead to trouble with other people, authority figures, or dangerous situations."
        world_facts_log = "World Facts\n\n"
        world_facts_log += "WORLD FACTS: - The story takes place in a small, run-down town in the southwestern United States in the late 20th century. - Technology is limited to what is commonly available in that time (no smartphones, no advanced surveillance systems). - The environment is grounded and realistic. No supernatural events exist except for the talking dog(rocket) and its ability. - The dog(rocket) can predict events only up to 30 seconds into the future. The predictions are always accurate but limited strictly to that time window. - The dog(rocket) cannot see beyond 30 seconds and cannot explain why events happen, only what will happen. - If other people discover the dog can talk or predict the future, both the boy and the dog(rocket) risk being taken away, studied, or separated. - Money is scarce for the boy’s family. Small amounts of cash can make a meaningful difference. - Actions have realistic consequences. Risky behavior can lead to trouble with other people, authority figures, or dangerous situations."
        Cycles = 1
        Variable = "I love Dogs"
        Variable += "and cats"
        print(Variable)


        test_temperature = .1
        text_cycle = 1
        max_tests = 1
        turn_counter = 1

        test_story_log = "I am a typical 1975 do whatever i want 18 year old kid who livesin my parents basement, they dont care that much about me, I love hanging out down there and smoking reefer. I was sitting in my parent's basement when a parcel appeared in front of me inside is a phone and a letter which reads: You have been chosen by the time council, this phone can transport you to any year, but if you are ever discovered to be a time traveler in any age, even by your own friends the time council will be very angry"
        test_world_facts = "The main character is named Danny \n The main character cannot reveal that he is a time traveler to anyone, else the time council will be very angry.\n Danny's phone can take him to any age"

        while text_cycle < max_tests:
            test_prompt = "What Model Are You?"
            Test_1 = generate_with_ollama(test_prompt, temperature= test_temperature)
            Test_2 = generate_with_ollama(test_prompt, model= "phi3.5:3.8b" )
            text_cycle += 1
            test_temperature += .05
            print("\n\n", Test_2, "\n", Test_1, "\n\n\n")




        strict_model = "mixtral:8x7b"
        free_model = "mixtral:8x7b"

        # Generate character_action
        Ai_Personality = "Choose a realistic action based on your personality and your memory"
        simulator_prompt_1 = "You are the simulation engine for an ai adventure, take the player's most recent action and simulate the result, " \
        "write in a present tense engaging third person style, stop simulating when it is time for the player to take another action"
        summary_prompt = "take the below text and summarize to raw plot points and scene descriptions, output the response raw, keep action and simulator seperate.  Player Action --"
        emotion_prompt = "Your job is to update the CURRENT PSYCHOLOGICAL PROFILE profile based on realistic behavior. The character is NOT heroic, NOT idealized, and NOT narratively optimized. They are flawed, impulsive, and self-interested. Their goals should reflect immediate desires, laziness, curiosity, or personal gain — not moral purpose.. Do not explain youself. \n\nUpdate Current psychological Profile based on your CURRENT PSYCHOLOGICAL PROFILE, LAST OUTCOME, LAST CHARACTER ACTION  --LAST CHARACTER ACTION--"

       
        seed_personality_prompt = "TASK\nGenerate a fictional personality.\n\nINPUT\nSEED CHARACTER ATTRIBUTES:\n", story_log, "WORLD FACTS", world_facts_log, "\n\nOUTPUT FORMAT\nWrite exactly three paragraphs.\nEach paragraph must be 3–5 sentences.\nParagraph 1: Background and identity including the character's name and approximate age.\nParagraph 2: Core personality traits.\nParagraph 3: Interests, habits, and inner motivations.\n\nCONSTRAINTS\nWrite only the personality description.\nDo not explain the task.\nDo not repeat the instructions.\nDo not include labels like 'Paragraph 1'.\nNever say 'I generated' or similar meta phrases."
        seed_personality = generate_with_ollama(seed_personality_prompt)
        print("--Seed Personality Prompt--\n\n", seed_personality_prompt)
        print("\n\n--Seed Personality Outcome--\n\n", seed_personality)

        seed_emotion_prompt = "TASK\nCreate a RAW psychological profile based on realistic behavior. The character is NOT inherently heroic, NOT idealized, and NOT narratively optimized.\n They are flawed, impulsive, and self-interested.\n Their goals should reflect immediate desires, laziness, curiosity, or personal gain — not moral purpose..\n Keep the profile concise\n SEED CHARACTER ATTRIBUTES:", story_log, "\n\nPersonality:\n", seed_personality, "\n\nOUTPUT FORMAT\n OUTPUT FORMAT CORE IDENTITY (DO NOT CHANGE): - Personality traits - Moral alignment - Baseline motivations CURRENT STATE (CAN CHANGE SLIGHTLY): - Wants (short-term only) - Current emotion - Story goals (immediate only) Each section header must be exactly as listed.\nCORE IDENTITY (DO NOT CHANGE): \n- Personality traits \n- Moral alignment \n- Baseline motivations CURRENT STATE (CAN CHANGE SLIGHTLY): \n- Wants (short-term only) \n- Current emotion \n- Story goals (immediate only)\n\nCONSTRAINTS\nWrite only the profile.\nDo not explain the task.\nDo not repeat the instructions.\nDo not refer to yourself.\nStop after CURRENT_EMOTION. PERSONALITY LOCK: You must directly use the provided Personality. Do NOT reinterpret, expand, or rewrite it. Extract traits only."
        seed_emotion = generate_with_ollama(seed_emotion_prompt)
        print("\n\n\n\n--Seed Emotion Prompt--\n\n", seed_emotion_prompt)
        print("\n\n--Seed Emotion Outcome--\n\n", seed_emotion)
        summarize_log = "Summary Log\n"


        max_turns = 5
        turn_counter = 1
        
    
        current_mood = random.randint(1, 8)
        character_actions_prompt = "Your job is to to output 5-8 concrete actions for  your character to take", seed_personality, "--Emotional Profile--", seed_emotion, "Current Situation Memory--", writing_instructions, "Current Character Mood:", mood[current_mood], "TASK \n Choose 5-8 concrete actions for your character to take based upon the EXAMPLE FORMAT\n\nEXAMPLE FORMAT:\n Action 1 (evil): The character secretly steals money from the table while the others are distracted. \n Action 2 (aggressive): The character slams their fist on the table and demands an explanation. \n Action 3 (cooperative): The character offers to help gather the scattered papers. \n Action 4 (cautious): The character slowly checks the hallway before stepping outside. \n Action 5 (social): The character asks the others what they think should happen next. \n Action 6 (unexpected): The character starts loudly singing to break the tension in the room.\n\n\n Create realistic, tangible actions that progress the story.\n Do not explain yourself.\n Actions must be realistic responses to the situation. \n Do not create supernatural or impossible actions unless the story already includes them.\n Actions must be immediate physical or spoken actions. \n Do not output thoughts, desires, or intentions. \n Each action must begin with the character performing the action. PERSONALITY CONSISTENCY RULE: All actions must reflect the character’s CORE IDENTITY. Do NOT generate actions that are noble, heroic, or responsible unless explicitly part of their personality. Prefer actions that are: - self-interested - impulsive - emotionally driven - practical for immediate gain\n"
        character_actions = generate_with_ollama(character_actions_prompt)
        print("\n\n\n\n--Character Action  options Prompt --\n\n", character_actions_prompt)
        print("\n\n--Character Action options  Outcome--\n\n", character_actions)
        
        character_action_prompt_first = "You are deciding what action a character will take in a story.\n\n CHARACTER PERSONALITY\n", seed_personality, "\n\n EMOTIONAL PROFILE\n", seed_emotion, "\n\n CURRENT MOOD\n", mood[current_mood], "\n\n CURRENT SITUATION\n", writing_instructions, "\n\n POSSIBLE ACTIONS\n", character_actions, "\n\n TASK\n Choose the ONE action the character is most likely to take.\n\n RULES\n - Choose only ONE action from the list.\n - Do not invent new actions.\n - The chosen action must match the character's personality, emotions, and situation.\n - Avoid repeating the previous action unless it makes strong sense.\n - Prefer actions that move the situation forward.\n\n OUTPUT FORMAT\n Output ONLY the chosen action exactly as written.\n Do not add explanations.\n"
        character_action = generate_with_ollama(character_action_prompt_first, model= strict_model, temperature = .4)
        print("\n\n\n\n--Character Action Prompt First--\n\n", character_action_prompt_first)
        print("\n\n--Character Action First Outcome--\n\n", character_action)


        npc_motive_prompt = "You are an NPC MOTIVE ENGINE for an interactive narrative simulation.\n Your job is to determine what each NPC currently present wants and what they intend to do next.\n RULES - Only include NPCs that are currently present in the scene.\n - Every NPC must have a clear goal and immediate intention.\n - NPCs must behave realistically.\n - NPCs cannot silently observe forever.\n - NPCs must either interact, act, or leave.\n - Do NOT narrate events.\n NPC STRUCTURE\n Name:\n Goal:\n Immediate intention:\n Attitude toward player:\n RECENT STORY EVENT\n", story_log, "WORLD FACTS", world_facts, "\nCURRENT PLOT PRESSURE\n", plot_points[current_plot_index], "\n LONG TERM MEMORY\n," "OUTPUT List the motives for each NPC currently in the scene. Do not list motives for the main character. Do not explain yourself or output extra text.\n If no NPCs are present return: NONE "
        npc_motive = generate_with_ollama(npc_motive_prompt, model= strict_model, temperature = .4)
        print("\n\n\n\n--NPC MOTIVE PROMOT--\n\n", npc_motive_prompt)
        print("\n\n--NPC MOTIVE Outcome--\n\n", npc_motive)


        scene_state_prompt = " You are a SCENE STATE TRACKER for a narrative simulation.\n Your job is to track the physical state of the current scene.\n RULES - Only track physical facts.\n - Do NOT narrate.\n - Do NOT invent new events.\n - Keep descriptions short and practical.\n - Characters cannot see through walls, tents, or solid objects.\n TRACK\n Location Visible characters\n Hidden characters\n Important objects\n Visibility conditions\n PREVIOUS SCENE STATE\n", story_log, "RECENT STORY EVENTS\n", story_log, "OUTPUT\n Update the scene state using the same structure.\n Only change things if the story events require it.\n "
        scene_state = generate_with_ollama(scene_state_prompt, model= strict_model, temperature = .2)
        print("\n\n\n\n--Scene State Prompt --\n\n", scene_state_prompt)
        print("\n\n--Scene State Outcome--\n\n", scene_state)

        director_prompt = ("You are a strict narrative simulator.\\nRECENT STORY EVENTS\\n", summarize_log, "\nYour job is to generate the NEXT immediate situation that should happen in the story.\n RULES - Describe a physical situation, interruption, discovery, or decision pressure.\n - Do NOT narrate the outcome.\n - Do NOT explain anything.\n - Do NOT repeat previous situations.\n - Avoid mysterious observers or supernatural forces unless the plot point includes them.\n - All events must directly involve ONLY elements present in SCENE STATE or explicitly introduced in RECENT STORY EVENTS.\n - Do NOT introduce new structures, locations, or objects unless they logically exist in the current scene state.\n - Only introduce elements consistent with CURRENT WORLD FACTS.\n - Each event must change the situation in a meaningful way (new information, new risk, or new opportunity).\n - Do NOT repeat similar interactions without escalation or a new outcome.\n CHARACTER ACTION must occur at the beggining of your output\n\n CURRENT WORLD FACTS", world_facts, "SCENE STATE", scene_state, "\nNPC MOTIVES\n", npc_motive,  "\nCHARACTER ACTION\n", character_action, "TASK:\n - Determine what actually happens physically.\n - Follow world rules strictly.\n - Do not narrate.\n - Do not be creative.\n", plot_point,  "OUTPUT FORMAT: Bullet list of factual events only. ")
        direction = generate_with_ollama(director_prompt, model= strict_model, temperature = .2)
        print("\n\n\n\n--Director Prompt --\n\n", director_prompt)
        print("\n\n--Director Outcome--\n\n", direction)

        
        simulator_prompt = "You are", "a narrator for an interactive narrative. Your job is to narrate based on the DIRECTOR PROMPT \n\n Use a present-tense, engaging third-person narrative.\\n Do not explain yourself, CONSTRAINTS\\n- Do NOT choose the next player action.\\n- Do NOT summarize or explain yourself.\\n Do NOT repeat your directives\\n" "- Write continuously until it makes sense for the player to act again.\\n- End the narrative with '__END__'\\n\\n\\n\\n STYLE RULES\\n Use clear physical narration. \\nDo not use poetic metaphors or symbolic language.\n NPCs should behave like real people. \nThey should speak, react, ask questions, or leave if ignored.\n They should not stare silently for long periods. \n Events should follow practical cause and effect.\n New characters or objects must have a clear reason for appearing \n\n\n Characters must obey the scene state.\n Characters cannot see things that are hidden from them. \nCharacters cannot appear or disappear without explanation.\nDo not describe emotions in the environment no ('whispering wind', 'anticipation in the air'). Describe only observable events and character thoughts. Keep descriptions practical and grounded. .\n\n\nNPC MOTIVES:", npc_motive, "World Facts(Simulation MUST not break world facts)", world_facts, "\nDIRECTOR PROMPT:", direction, "\nTASK\n Narrate what would happen next based on the DIRECTOR PROMPT, do not make your own narrative, do not explain yourself"        
        simulator = generate_with_ollama(simulator_prompt, model=free_model, temperature=0.7)
        print("\n\n\n\n--Simulator Prompt --\n\n", simulator_prompt)
        print("\n\n--Simulator Outcome--\n\n", simulator)
        
       
             
            
        summarize_prompt = ( "Summarize the following story update into as little words as you can. Do not write code, programming syntax, or explanations. Output plain text only. Only keep information that may matter for future events. Ignore narration, descriptive prose, and basic.\n\n", "STORY_UPDATE:", simulator, "Write 2 to 4 very short bullet style lines describing what actually happened. Each line should describe one concrete event, discovery, or interaction. Keep every line under 20 words. Begin each line with '-'\nEnd the response with '__END__'" )
        summarize = generate_with_ollama(summarize_prompt)
        print("\n\n\n\n--Summarize Prompt --\n\n", summarize_prompt)
        print("\n\n--Summarize Outcome--\n\n", summarize)

        world_facts_prompt = ( "You are a WORLD STATE RECORDER. Your job is to extract ONLY objective world facts that permanently changed. RULES: - Write short factual statements. - No narration. - No metaphors. - No speculation. - No emotions. - Do NOT repeat facts that already exist. - Only include NEW persistent facts CHARACTER ACTION:", character_action, "SIMULATOR RESULT:", simulator, "CURRENT EMOTION:", seed_emotion, "CURRENT WORLD FACTS", world_facts_log, "Return ONLY the new facts. If no new facts occurred, return: NONE\n Do not explain youself, Do not add any extra text, in the next part of the story the dog should reveal his abilities to the boy if he hasnt already ")
        world_facts = generate_with_ollama(world_facts_prompt, model= strict_model, temperature = .4)
        world_facts_log += world_facts
        print("\n\n\n\n--World Facts Prompt --\n\n", world_facts_prompt)
        print("\n\n--World Facts Outcome--\n\n", world_facts)
        print("\n\n--World Facts Log--\n\n", world_facts_log)

        story_log += "Personality" + character_action + "\n\n"
        story_log += "Simulator" + simulator + "\n\n"
        
        summarize_log = "Summary Log\n"
        summarize_log += summarize + "\n"
        Cycles +=1
        print("\n\n\n", Cycles, "\n\n\n")
        #------------------------------------------



        #Second Gen Cycle
        #-------------------------------------------
        
        emotion_combined_first = emotion_prompt, character_action, "--LAST OUTCOME--", simulator, "--CURRENT PSYCHOLOGICAL PROFILE--", seed_emotion, "CORE IDENTITY RULES:\n - The CORE IDENTITY is PERMANENT and must NEVER change.\n - Do NOT reinterpret, expand, or evolve the character's personality. \n- All updates must stay consistent with this identity. DRIFT PREVENTION: \n- If new events suggest responsibility, morality, or heroism, IGNORE that shift unless it directly aligns with the core identity.\n - The character does NOT become more noble over time. Make sure you retain formatting and only make small changes in the emotional profile, small character progression no overhauls. Output your response with no explanation. Do not increase the word count" 
        emotion = generate_with_ollama(emotion_combined_first, model= strict_model, temperature= .4)
        print("\n\n\n\n--Emotion First Prompt--\n\n", emotion_combined_first)
        print("\n\n--Emotion First Outcome--\n\n", emotion)

        current_mood = random.randint(1, 8)
        current_mood = random.randint(1, 8)
        character_actions_prompt = "Your job is to to output 5-8 concrete actions for  your character to take", seed_personality, "--Emotional Profile--", seed_emotion, "Current Situation Memory--", simulator, "Last Action taken", character_action, "Current Character Mood:", mood[current_mood], "TASK \n Choose 5-8 concrete actions for your character to take based upon the EXAMPLE FORMAT\n\nEXAMPLE FORMAT:\n Action 1 (evil): The character secretly steals money from the table while the others are distracted. \n Action 2 (aggressive): The character slams their fist on the table and demands an explanation. \n Action 3 (cooperative): The character offers to help gather the scattered papers. \n Action 4 (cautious): The character slowly checks the hallway before stepping outside. \n Action 5 (social): The character asks the others what they think should happen next. \n Action 6 (unexpected): The character starts loudly singing to break the tension in the room.\n\n\n Create realistic, tangible actions that progress the story.\n Do not explain yourself.\n Actions must be realistic responses to the situation. \n Do not create supernatural or impossible actions unless the story already includes them.\n Actions must be immediate physical or spoken actions. \n Do not output thoughts, desires, or intentions. \n Each action must begin with the character performing the action.\n PERSONALITY CONSISTENCY RULE: All actions must reflect the character’s CORE IDENTITY. Do NOT generate actions that are noble, heroic, or responsible unless explicitly part of their personality. Prefer actions that are: - self-interested - impulsive - emotionally driven - practical for immediate gain"
        character_actions = generate_with_ollama(character_actions_prompt, model= strict_model, temperature=.4)
        print("\n\n\n\n--Character Action  options Prompt --\n\n", character_actions_prompt)
        print("\n\n--Character Action options  Outcome--\n\n", character_actions)

        
        character_action_prompt_first = "You are deciding what action a character will take in a story.\n\n CHARACTER PERSONALITY\n", seed_personality, "\n\n EMOTIONAL PROFILE\n", emotion, "\n\n CURRENT MOOD\n", mood[current_mood], "\n\n CURRENT SITUATION\n", simulator, "\n\n LAST ACTION TAKEN\n", character_action, "\n\n POSSIBLE ACTIONS\n", character_actions, "\n\n TASK\n Choose the ONE action the character is most likely to take.\n\n RULES\n - Choose only ONE action from the list.\n - Do not invent new actions.\n - The chosen action must match the character's personality, emotions, and situation.\n - Avoid repeating the previous action unless it makes strong sense.\n - Prefer actions that move the situation forward.\n\n OUTPUT FORMAT\n Output ONLY the chosen action exactly as written.\n Do not add explanations.\n"
        character_action = generate_with_ollama(character_action_prompt_first, model= strict_model, temperature = .4)
        print("\n\n\n\n--Character Action Prompt First--\n\n", character_action_prompt_first)
        print("\n\n--Character Action First Outcome--\n\n", character_action)

        npc_motive_prompt = "You are an NPC MOTIVE ENGINE for an interactive narrative simulation.\n Your job is to determine what each NPC currently visible in the scene wants and what they intend to do next.\n RULES - Only include NPCs that are currently present in the scene.\n - Every NPC must have a clear goal and immediate intention.\n - NPCs must behave realistically.\n - NPCs cannot silently observe forever.\n - NPCs must either interact, act, or leave.\n - Do NOT narrate events.\n NPC STRUCTURE\n Name:\n Goal:\n Immediate intention:\n Attitude toward player:\n RECENT STORY EVENT\n", simulator, "WORLD FACTS", world_facts, "\nCURRENT PLOT PRESSURE\n", plot_points[current_plot_index], "\n LONG TERM MEMORY\n," "OUTPUT List the motives for each NPC currently in the scene. Do not list motives for the main character. Do not explain yourself or output extra text.\n Do not include characters unless the are in the RECENT STORY EVENT \n If no NPCs are present return: NONE "
        npc_motive = generate_with_ollama(npc_motive_prompt, model= strict_model, temperature = .4)
        print("\n\n\n\n--NPC MOTIVE PROMOT--\n\n", npc_motive_prompt)
        print("\n\n--NPC MOTIVE Outcome--\n\n", npc_motive)

        scene_state_prompt = " You are a SCENE STATE TRACKER for a narrative simulation.\n Your job is to track the physical state of the current scene.\n RULES - Only track physical facts.\n - Do NOT narrate.\n - Do NOT invent new events.\n - Keep descriptions short and practical.\n - Characters cannot see through walls, tents, or solid objects.\n TRACK\n Location Visible characters\n Hidden characters\n Important objects\n Visibility conditions\n PREVIOUS SCENE STATE\n", story_log, "RECENT STORY EVENTS\n", story_log, "OUTPUT\n Update the scene state using the same structure.\n Only change things if the story events require it.\n "
        scene_state = generate_with_ollama(scene_state_prompt, model=strict_model, temperature = .4)
        print("\n\n\n\n--Scene State Prompt --\n\n", scene_state_prompt)
        print("\n\n--Scene State Outcome--\n\n", scene_state)

        director_prompt = ("You are a strict narrative simulator.\\nRECENT STORY EVENTS\\n", summarize_log, "\nYour job is to generate the NEXT immediate situation that should happen in the story.\n RULES - Describe a physical situation, interruption, discovery, or decision pressure.\n - Do NOT narrate the outcome.\n - Do NOT explain anything.\n - Do NOT repeat previous situations.\n - Avoid mysterious observers or supernatural forces unless the plot point includes them.\n - All events must directly involve ONLY elements present in SCENE STATE or explicitly introduced in RECENT STORY EVENTS.\n - Do NOT introduce new structures, locations, or objects unless they logically exist in the current scene state.\n - Only introduce elements consistent with CURRENT WORLD FACTS.\n - Each event must change the situation in a meaningful way (new information, new risk, or new opportunity).\n - Do NOT repeat similar interactions without escalation or a new outcome.\n CHARACTER ACTION must occur at the beggining of your output\n\n CURRENT WORLD FACTS", world_facts, "SCENE STATE", scene_state, "\nNPC MOTIVES\n", npc_motive,  "\nCHARACTER ACTION\n", character_action, "TASK:\n - Determine what actually happens physically.\n - Follow world rules strictly.\n - Do not narrate.\n - Do not be creative.\n OUTPUT FORMAT: Bullet list of factual events only. ")
        direction = generate_with_ollama(director_prompt, model= strict_model, temperature = .2)
        print("\n\n\n\n--Director Prompt --\n\n", director_prompt)
        print("\n\n--Director Outcome--\n\n", direction)

        
        simulator_prompt = "You are", "a narrator for an interactive narrative. Your job is to narrate based on the DIRECTOR PROMPT \n\n Use a present-tense, engaging third-person narrative.\\n Do not explain yourself, CONSTRAINTS\\n- Do NOT choose the next player action.\\n- Do NOT summarize or explain yourself.\\n Do NOT repeat your directives\\n" "- Write continuously until it makes sense for the player to act again.\\n- End the narrative with '__END__'\\n\\n\\n\\n STYLE RULES\\n Use clear physical narration. \\nDo not use poetic metaphors or symbolic language.\n NPCs should behave like real people. \nThey should speak, react, ask questions, or leave if ignored.\n They should not stare silently for long periods. \n Events should follow practical cause and effect.\n New characters or objects must have a clear reason for appearing.\n Supernatural events should not occur unless already established or they strongly fit the scene. \n\n\n Characters must obey the scene state.\n Characters cannot see things that are hidden from them. \nCharacters cannot appear or disappear without explanation.\nDo not describe emotions in the environment no ('whispering wind', 'anticipation in the air'). Describe only observable events and character thoughts. Keep descriptions practical and grounded. .\n\n\nNPC MOTIVES:", npc_motive, "World Facts(Simulation MUST not break world facts)", world_facts,  "SCENE STATE", scene_state, "\nDIRECTOR PROMPT:", direction, "\nTASK\n Narrate what would happen next based on the DIRECTOR PROMPT, do not make your own narrative, do not explain yourself"        
        simulator = generate_with_ollama(simulator_prompt, model=free_model, temperature=0.7)
        print("\n\n\n\n--Simulator Prompt --\n\n", simulator_prompt)
        print("\n\n--Simulator Outcome--\n\n", simulator)
        
        

        summarize_prompt = ( "Summarize the following story update into as little words as you can. Do not write code, programming syntax, or explanations. Output plain text only. Only keep information that may matter for future events. Ignore narration, descriptive prose, and basic.\n\n", "STORY_UPDATE:", character_action, simulator, "Write 2 to 4 very short bullet style lines describing what actually happened. Each line should describe one concrete event, discovery, or interaction. Keep every line under 20 words. Begin each line with '- '.", "End the response with '__END__'" )
        summarize = generate_with_ollama(summarize_prompt, model= strict_model, temperature = .4)
        print("\n\n\n\n--Summarize Prompt --\n\n", summarize_prompt)
        print("\n\n--Summarize Outcome--\n\n", summarize)

        world_facts_prompt = ( "You are a WORLD STATE RECORDER. Your job is to extract ONLY objective world facts that permanently changed. RULES: - Write short factual statements. - No narration. - No metaphors. - No speculation. - No emotions. - Do NOT repeat facts that already exist. - Only include NEW persistent facts CHARACTER ACTION:", character_action, "SIMULATOR RESULT:", simulator, "CURRENT EMOTION:", emotion, "CURRENT WORLD FACTS", world_facts_log, "Return ONLY the new facts. If no new facts occurred, return: NONE\n Do not explain youself, Do not add any extra text, in the next part of the story the dog should reveal his abilities to the boy if he hasnt already ")
        world_facts = generate_with_ollama(world_facts_prompt, model= strict_model, temperature = .2)
        world_facts_log += world_facts
        print("\n\n\n\n--World Facts Prompt --\n\n", world_facts_prompt)
        print("\n\n--World Facts Outcome--\n\n", world_facts)

        story_log += "Personality" + character_action + "\n\n"
        story_log += "Simulator" + simulator + "\n\n"
        summarize_log = "Summary Log\n"
        summarize_log += summarize + "\n"
        Cycles +=1
        print("\n\n\n", Cycles, "\n\n\n")
        #--------------------------------------------


        simulator_last_three = "Start"
        story_summary_log = "Start"


        #--------------------------------------------
        simulator_count = 0
        turn_counter = 0
    while turn_counter < max_turns:
        emotion_combined = emotion_prompt, character_action, "--LAST OUTCOME--", simulator, "--CURRENT PSYCHOLOGICAL PROFILE--", emotion, "Make sure you retain formatting and only make small changes in the emotional profile, small character progression no overhauls. Output your response with no explanation. Do not increase the word count" 
        emotion = generate_with_ollama(emotion_combined, model= strict_model, temperature = .4)
        print("\n\n\n\n--Emotion First Prompt--\n\n", emotion_combined)
        print("\n\n--Emotion First Outcome--\n\n", emotion)

        current_mood = random.randint(1, 8)
        character_actions_prompt = "Your job is to to output 5-8 concrete actions for  your character to take", seed_personality, "--Emotional Profile--", emotion, "Current Situation Memory--", simulator, "Last Action taken", character_action, "Current Character Mood:", mood[current_mood], "TASK \n Choose 5-8 concrete actions for your character to take based upon the EXAMPLE FORMAT\n\nEXAMPLE FORMAT:\n Action 1 (evil): The character secretly steals money from the table while the others are distracted. \n Action 2 (aggressive): The character slams their fist on the table and demands an explanation. \n Action 3 (cooperative): The character offers to help gather the scattered papers. \n Action 4 (cautious): The character slowly checks the hallway before stepping outside. \n Action 5 (social): The character asks the others what they think should happen next. \n Action 6 (unexpected): The character starts loudly singing to break the tension in the room.\n\n\n Create realistic, tangible actions that progress the story.\n Do not explain yourself.\n Actions must be realistic responses to the situation. \n Do not create supernatural or impossible actions unless the story already includes them.\n Actions must be immediate physical or spoken actions. \n Do not output thoughts, desires, or intentions. \n Each action must begin with the character performing the action.\n PERSONALITY CONSISTENCY RULE: All actions must reflect the character’s CORE IDENTITY. Do NOT generate actions that are noble, heroic, or responsible unless explicitly part of their personality. Prefer actions that are: - self-interested - impulsive - emotionally driven - practical for immediate gain"
        character_actions = generate_with_ollama(character_actions_prompt, model= strict_model, temperature = .4)
        print("\n\n\n\n--Character Action  options Prompt --\n\n", character_actions_prompt)
        print("\n\n--Character Action options  Outcome--\n\n", character_actions)

        
        character_action_prompt_first = "You are deciding what action a character will take in a story.\n\n CHARACTER PERSONALITY\n", seed_personality, "\n\n EMOTIONAL PROFILE\n", seed_emotion, "\n\n CURRENT MOOD\n", mood[current_mood], "\n\n CURRENT SITUATION\n", writing_instructions, "\n\n LAST ACTION TAKEN\n", character_action, "\n\n POSSIBLE ACTIONS\n", character_actions, "\n\n TASK\n Choose the ONE action the character is most likely to take.\n\n RULES\n - Choose only ONE action from the list.\n - Do not invent new actions.\n - The chosen action must match the character's personality, emotions, and situation.\n - Avoid repeating the previous action unless it makes strong sense.\n - Prefer actions that move the situation forward.\n\n OUTPUT FORMAT\n Output ONLY the chosen action exactly as written.\n Do not add explanations.\n"
        character_action = generate_with_ollama(character_action_prompt_first, model= strict_model, temperature = .4)
        print("\n\n\n\n--Character Action Prompt First--\n\n", character_action_prompt_first)
        print("\n\n--Character Action First Outcome--\n\n", character_action)

        npc_motive_prompt = "You are an NPC MOTIVE ENGINE for an interactive narrative simulation.\n Your job is to determine what each NPC currently present wants and what they intend to do next.\n RULES - Only include NPCs that are currently present in the scene.\n - Every NPC must have a clear goal and immediate intention.\n - NPCs must behave realistically.\n - NPCs cannot silently observe forever.\n - NPCs must either interact, act, or leave.\n - Do NOT narrate events.\n NPC STRUCTURE\n Name:\n Goal:\n Immediate intention:\n Attitude toward player:\n RECENT STORY EVENT\n", simulator, "WORLD FACTS", world_facts, "\nCURRENT PLOT PRESSURE\n", plot_points[current_plot_index], "\n LONG TERM MEMORY\n," "OUTPUT List the motives for each NPC currently in the scene. Do not list motives for the main character. Do not explain yourself or output extra text.\n If no NPCs are present return: NONE "
        npc_motive = generate_with_ollama(npc_motive_prompt, model= strict_model, temperature = .4)
        print("\n\n\n\n--NPC MOTIVE PROMOT--\n\n", npc_motive_prompt)
        print("\n\n--NPC MOTIVE Outcome--\n\n", npc_motive)

        scene_state_prompt = " You are a SCENE STATE TRACKER for a narrative simulation.\n Your job is to track the physical state of the current scene.\n RULES - Only track physical facts.\n - Do NOT narrate.\n - Do NOT invent new events.\n - Keep descriptions short and practical.\n - Characters cannot see through walls, tents, or solid objects.\n TRACK\n Location Visible characters\n Hidden characters\n Important objects\n Visibility conditions\n PREVIOUS SCENE STATE\n", story_log, "RECENT STORY EVENTS\n", story_log, "OUTPUT\n Update the scene state using the same structure.\n Only change things if the story events require it.\n "
        scene_state = generate_with_ollama(scene_state_prompt, model= strict_model, temperature= .4)
        print("\n\n\n\n--Scene State Prompt --\n\n", scene_state_prompt)
        print("\n\n--Scene State Outcome--\n\n", scene_state)

        director_prompt = ("You are a strict narrative simulator.\\nRECENT STORY EVENTS\\n", summarize_log, "\nYour job is to generate the NEXT immediate situation that should happen in the story.\n RULES - Describe a physical situation, interruption, discovery, or decision pressure.\n - Do NOT narrate the outcome.\n - Do NOT explain anything.\n - Do NOT repeat previous situations.\n - Avoid mysterious observers or supernatural forces unless the plot point includes them.\n - All events must directly involve ONLY elements present in SCENE STATE or explicitly introduced in RECENT STORY EVENTS.\n - Do NOT introduce new structures, locations, or objects unless they logically exist in the current scene state.\n - Only introduce elements consistent with CURRENT WORLD FACTS.\n - Each event must change the situation in a meaningful way (new information, new risk, or new opportunity).\n - Do NOT repeat similar interactions without escalation or a new outcome.\n CHARACTER ACTION must occur at the beggining of your output\n\n CURRENT WORLD FACTS", world_facts, "SCENE STATE", scene_state, "\nNPC MOTIVES\n", npc_motive,  "\nCHARACTER ACTION\n", character_action, "TASK:\n - Determine what actually happens physically.\n - Follow world rules strictly.\n - Do not narrate.\n - Do not be creative.\n", plot_point, "OUTPUT FORMAT: Bullet list of factual events only. ")
        direction = generate_with_ollama(director_prompt, model= strict_model, temperature = .2)
        print("\n\n\n\n--Director Prompt --\n\n", director_prompt)
        print("\n\n--Director Outcome--\n\n", direction)

        
        simulator_prompt = "You are", "a narrator for an interactive narrative. Your job is to narrate based on the DIRECTOR PROMPT \n\n Use a present-tense, engaging third-person narrative.\\n Do not explain yourself, CONSTRAINTS\\n- Do NOT choose the next player action.\\n- Do NOT summarize or explain yourself.\\n Do NOT repeat your directives\\n" "- Write continuously until it makes sense for the player to act again.\\n- End the narrative with '__END__'\\n\\n\\n\\n STYLE RULES\\n Use clear physical narration. \\nDo not use poetic metaphors or symbolic language.\n NPCs should behave like real people. \nThey should speak, react, ask questions, or leave if ignored.\n They should not stare silently for long periods. \n Events should follow practical cause and effect.\n New characters or objects must have a clear reason for appearing.\n Supernatural events should not occur unless already established or they strongly fit the scene. \n\n\n Characters must obey the scene state.\n Characters cannot see things that are hidden from them. \nCharacters cannot appear or disappear without explanation.\nDo not describe emotions in the environment no ('whispering wind', 'anticipation in the air'). Describe only observable events and character thoughts. Keep descriptions practical and grounded. .\n\n\nNPC MOTIVES:", npc_motive, "World Facts(Simulation MUST not break world facts)", world_facts,  "SCENE STATE", scene_state, "\nDIRECTOR PROMPT:", direction, "\nTASK\n Narrate what would happen next based on the DIRECTOR PROMPT, do not make your own narrative, do not explain yourself"        
        simulator = generate_with_ollama(simulator_prompt, model=free_model, temperature=0.7)
        print("\n\n\n\n--Simulator Prompt --\n\n", simulator_prompt)
        print("\n\n--Simulator Outcome--\n\n", simulator)
        
        

        summarize_prompt = ( "Summarize the following story update into as little words as you can. Do not write code, programming syntax, or explanations. Output plain text only. Only keep information that may matter for future events. Ignore narration, descriptive prose, and basic.\n\n", "STORY_UPDATE:", character_action, simulator, "Write 2 to 4 very short bullet style lines describing what actually happened. Each line should describe one concrete event, discovery, or interaction. Keep every line under 20 words. Begin each line with '- '.", "End the response with '__END__'" )
        summarize = generate_with_ollama(summarize_prompt, model= strict_model, temperature = .4)
        print("\n\n\n\n--Summarize Prompt --\n\n", summarize_prompt)
        print("\n\n--Summarize Outcome--\n\n", summarize)
        summarize_log += summarize + "\n"
        print("\n\n--Summarize Log--\n\n", summarize_log)


        world_facts_prompt = ( "You are a WORLD STATE RECORDER. Your job is to extract ONLY objective world facts that permanently changed. RULES: - Write short factual statements. - No narration. - No metaphors. - No speculation. - No emotions. - Do NOT repeat facts that already exist. - Only include NEW persistent facts CHARACTER ACTION:", character_action, "SIMULATOR RESULT:", simulator, "CURRENT EMOTION:", emotion, "CURRENT WORLD FACTS", world_facts_log, "Return ONLY the new facts. If no new facts occurred, return: NONE\n Do not explain youself, Do not add any extra text, in the next part of the story the dog should reveal his abilities to the boy if he hasnt already ")

        world_facts = generate_with_ollama(world_facts_prompt, model= strict_model, temperature = .2)
        world_facts_log += world_facts
        print("\n\n\n\n--World Facts Prompt --\n\n", world_facts_prompt)
        print("\n\n--World Facts Outcome--\n\n", world_facts)
        print("\n\n--World Facts Log--\n\n", world_facts_log)

        story_log += "Personality" + character_action + "\n\n"
        story_log += "Simulator" + simulator + "\n\n"
        
        
        Cycles +=1
        turn_counter +=1
        print("\n\n\n", Cycles, "\n\n\n")
        
        current_turn += 1
        if current_turn == plot_frequency:
            current_plot_index +=1
            current_turn = 0
            plot_point = "- The following plot point MUST occur in this step and be shown through physical events:" + plot_points[current_plot_index]
        else:
         plot_point = "\n"





        simulator_last_three += simulator
        simulator_count += 1
        if simulator_count == 6:
            story_summary_prompt = "you are the story summarizer for an ai text adventure.\n\n STORY LOG :", simulator_last_three, "Go over major plot points and actions, if characters went in circles or it didnt make sense make that clear, be concise"
            story_summary = generate_with_ollama(story_summary_prompt, model= strict_model)
            story_summary_log += "\n\n\n\nNew Block\n" + story_summary
            simulator_count = 0
            simulator_last_three = "Story Log\n\n"


        #--------------------------------------------
        #--------------------------------------------
        print(story_summary_log)
        

       

        

        
 

        


 
    # Get current situation (last paragraph before actions)
    current_situation = story_log.split("\n\n")[-1].strip() if "\n\n" in story_log else story_log.strip()

    return jsonify({
        'story_log': story_log,
        'simulator_log': summarized_log,
        'current_situation': current_situation
        
    })

if __name__ == '__main__':
    app.run(debug=True)

    
