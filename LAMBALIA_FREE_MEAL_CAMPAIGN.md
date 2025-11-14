# 🍽️ LAMBALIA FREE MEAL LAUNCH CAMPAIGN STRATEGY
## Champaign, IL | Saturday [3 Weeks from Now] | 150 Free Meals

---

# 🎯 CAMPAIGN OVERVIEW

**Campaign Name:** Lambalia Free Meal Launch
**Location:** Champaign, Illinois
**Date:** Saturday, [DATE - 3 weeks from now]
**Offer:** FREE Nigerian Jollof Rice with Fried Chicken & Fried Plantains
**Target:** 150 first signups
**Home Chefs:** 3 participating chefs (50 meals each)
**Cost:** You provide ingredients + pay chefs

---

# 🔐 UNIQUE CODE SYSTEM (Prevent Duplicate Signups)

## System Design:

**Code Format:** `LAMB-XXXX-Y`
- LAMB = Lambalia prefix
- XXXX = 4-digit unique number (0001-0150)
- Y = Chef assignment (A, B, or C)

**Example Codes:**
- `LAMB-0001-A` (First signup, Chef A)
- `LAMB-0052-B` (52nd signup, Chef B)
- `LAMB-0150-C` (Last signup, Chef C)

---

## Code Generation Methods:

### **Option 1: Simple Google Forms + Spreadsheet (FREE - RECOMMENDED)**

**Step-by-Step:**

1. **Create Google Form:**
   - Go to forms.google.com
   - Create form: "Lambalia Free Meal Registration"

2. **Form Fields:**
   ```
   - Full Name* (required)
   - Phone Number* (required)
   - Email Address* (required)
   - Have you already registered? (Yes/No)*
   - Preferred Pickup Time: (12-2 PM / 2-4 PM / 4-6 PM)
   - Any food allergies? (text field)
   ```

3. **Response Spreadsheet Setup:**
   - Form responses auto-populate Google Sheet
   - Add column: "Unique Code"
   - Add column: "Assigned Chef"
   - Add column: "Pickup Status" (Scheduled/Picked Up/No-Show)

4. **Auto-Generate Codes (Google Sheets Formula):**
   
   In the "Unique Code" column (assuming responses start in Row 2):
   ```
   =IF(B2<>"", "LAMB-" & TEXT(ROW()-1, "0000") & "-" & IF(MOD(ROW()-1,3)=1,"A",IF(MOD(ROW()-1,3)=2,"B","C")), "")
   ```

   This formula:
   - Generates unique sequential codes
   - Auto-assigns to Chef A, B, or C in rotation
   - Only generates if there's a name in the row

5. **Prevent Duplicates:**
   - Use Google Forms "Response validation"
   - For Phone Number field: Set to "Regular expression" → "Matches" → `^\d{10}$`
   - For Email field: Set to "Regular expression" → "Contains" → `@`
   - Manually check for duplicate phone/email before confirming

6. **Auto-Send Confirmation:**
   - Use Google Forms add-on: "Email Notifications for Forms" (FREE)
   - Auto-email each signup with their unique code
   - Email template below

---

### **Option 2: Simple Website Signup Form (If you have tech help)**

Create simple signup page at: `lambalia.com/freemeal`

**Features:**
- Check for duplicate email/phone in database before allowing signup
- Auto-generate unique code
- Send confirmation email automatically
- Real-time counter showing spots remaining
- Stop accepting signups after 150

**Tech Stack:**
- Backend: Simple FastAPI endpoint
- Database: MongoDB (you already have this)
- Email: SMTP service you set up for 2FA

---

### **Option 3: Text-Based RSVP (Radio-Friendly)**

**For Radio Promotion:**
"Text FREEFOOD to (XXX) XXX-XXXX to claim your free meal!"

**How it works:**
- Use Twilio (affordable, $1 for phone number + $0.0075 per SMS)
- Auto-respond with registration link
- Track phone numbers to prevent duplicates
- Send unique code via text

**Twilio Setup Cost:**
- Phone number: $1/month
- 150 signups × 2 texts each = 300 texts × $0.0075 = $2.25
- **Total: ~$3-4 for entire campaign**

---

## RECOMMENDED APPROACH:

**Use Google Forms + Manual Verification**

**Why:**
- FREE (no cost)
- Easy to set up (30 minutes)
- Shareable link for radio/flyers
- Auto-generates codes
- You can manually check for duplicates
- Export to Excel for chef coordination

---

# 📧 CONFIRMATION EMAIL TEMPLATE

**Subject:** Your Lambalia Free Meal is Reserved! Code: [UNIQUE CODE]

**Email Body:**

```
🎉 Congratulations, [NAME]!

You're registered for Lambalia's FREE MEAL LAUNCH!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR MEAL:
Nigerian Jollof Rice with Fried Chicken 
& Fried Plantains 🍗🍚🍌
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 YOUR UNIQUE CODE: [LAMB-XXXX-Y]

📅 PICKUP DATE: Saturday, [DATE]
⏰ PICKUP TIME: [TIME SLOT]
👨‍🍳 YOUR CHEF: Chef [A/B/C]
📍 PICKUP LOCATION: [Chef's Address or Central Location]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANT:
✓ Save this email! You'll need your code to pick up.
✓ Bring your code (screenshot this email or write it down)
✓ One meal per code (please don't share your code)
✓ If you can't make it, please text us so we can give your spot to someone else

QUESTIONS?
Call/Text: [YOUR PHONE NUMBER]
Email: hello@lambalia.com

See you Saturday!
The Lambalia Team

P.S. - After trying your free meal, sign up at lambalia.com to order more amazing home-cooked meals! 💚

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is a one-time promotional offer.
Visit lambalia.com to learn more about our platform.
```

---

# 📻 RADIO AD SCRIPTS

## **SCRIPT 1: 30-Second Spot (WDWS 1400 AM)**

```
[UPBEAT AFRICAN MUSIC INTRO - 3 seconds]

ANNOUNCER: "Champaign! This Saturday only - get a FREE authentic Nigerian meal from Lambalia!

That's Jollof Rice with Fried Chicken and Plantains. Completely FREE!

First 150 people to sign up at Lambalia.com/freemeal get this amazing meal. No catch. Just great food.

Lambalia - connecting you with authentic home-cooked meals from around the world. Right here in Champaign.

Sign up NOW at Lambalia.com/freemeal. That's Lambalia.com/freemeal.

First 150 only. Don't miss out!"

[MUSIC OUT]
```

**Frequency:** Run 3x daily for 2 weeks (42 total spots)

---

## **SCRIPT 2: 60-Second Spot (WDWS 1400 AM)**

```
[WARM AFRICAN MUSIC - 5 seconds]

ANNOUNCER: "Hey Champaign-Urbana, have you heard about Lambalia?

It's a new food platform connecting you with home chefs from over 80 countries - right here in our community!

And this Saturday, we're celebrating our launch with FREE FOOD!

The first 150 people to register online get a completely FREE authentic Nigerian meal: Jollof Rice with Fried Chicken and Fried Plantains. Made fresh by local home chefs.

No purchase necessary. No credit card. Just register at Lambalia.com/freemeal and you'll get a unique pickup code.

This is real, authentic Nigerian cooking. The kind you can't get at restaurants. Made by Nigerian home chefs right here in Champaign.

Why are we doing this? Because Lambalia helps home cooks earn money while sharing their cultural cuisine. And we want YOU to taste the difference.

So visit Lambalia.com/freemeal right now. That's L-A-M-B-A-L-I-A dot com slash freemeal.

First 150 signups get a free meal this Saturday. When they're gone, they're gone!

Lambalia - Your passport to world cuisine, right here in Champaign."

[MUSIC OUT]
```

**Frequency:** Run 2x daily for 2 weeks (28 total spots)

---

## **SCRIPT 3: Live Read (Morning Show)**

```
"Good morning! I've got something exciting for you. This Saturday, a new platform called Lambalia is launching in Champaign with FREE FOOD!

If you're one of the first 150 people to register online, you get a completely free authentic Nigerian meal - we're talking Jollof Rice, Fried Chicken, Fried Plantains. This is the real deal, folks.

I actually tried this meal yesterday [NOTE: Schedule a tasting for DJ], and it's AMAZING. You can't get this at any restaurant in town.

Just go to Lambalia.com/freemeal and sign up. You'll get a unique code for pickup this Saturday.

Lambalia is all about connecting you with home chefs from around the world. Right here in Champaign. It's like traveling through food without leaving town.

So go to Lambalia.com/freemeal right now. First 150 get free food Saturday. Don't sleep on this!"
```

**Schedule:** 2-3 live reads during morning drive time (7-9 AM)

---

# 🎨 FLYER DESIGN CONTENT

## **Flyer Layout (8.5" x 11")**

### **TOP SECTION (Eye-catching):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 FREE MEAL! 🎉
LAMBALIA LAUNCH CELEBRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### **CENTER IMAGE:**
[Large photo of Nigerian Jollof Rice with Fried Chicken and Plantains]

### **MAIN OFFER:**
```
🍗 Authentic Nigerian Jollof Rice
🍚 Fried Chicken
🍌 Fried Plantains

100% FREE!
NO PURCHASE REQUIRED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 THIS SATURDAY ONLY
[DATE]

⏰ PICKUP: 12 PM - 6 PM

📍 [PICKUP LOCATION]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIRST 150 SIGNUPS ONLY!
```

### **CALL TO ACTION:**
```
HOW TO GET YOUR FREE MEAL:

1️⃣ Visit: lambalia.com/freemeal
2️⃣ Register (takes 1 minute)
3️⃣ Get your unique pickup code
4️⃣ Pick up Saturday with your code!

OR TEXT "FREEFOOD" TO [NUMBER]
```

### **BOTTOM SECTION:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT IS LAMBALIA?

A platform connecting you with home chefs 
from 80+ countries. Authentic home-cooked 
meals delivered to your door!

lambalia.com | lambalia.app

@lambalia on Instagram & TikTok

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[QR CODE to lambalia.com/freemeal]

Scan to Register →
```

---

## **Where to Distribute Flyers:**

**Champaign Locations (300-500 flyers):**
- University of Illinois Student Union
- Coffee shops (Espresso Royale, Cafe Kopi, etc.)
- Libraries (Champaign Public Library)
- Grocery stores bulletin boards
- Apartment complex common areas
- Champaign Chamber of Commerce
- Local barbershops & salons
- University housing areas
- Altgeld Hall (UIUC)
- Illini Union
- Campus Recreation Center
- International Student Services office

---

# 🛍️ TAKEAWAY BAG DESIGN

## **Bag Specifications:**

**Size:** 10" x 13" x 5" (Standard takeout bag)
**Material:** Kraft paper or recyclable
**Quantity:** 150 bags
**Cost:** ~$50-75 for 150 custom bags (online printing)

---

## **Bag Design - Side 1 (Front):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[LAMBALIA LOGO - Large, centered]

YOUR KITCHEN = YOUR BUSINESS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thank you for trying Lambalia!

This FREE meal was prepared by a local 
home chef from our Champaign community.

Enjoyed this? Order more at:
lambalia.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## **Bag Design - Side 2 (Back):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WANT TO EARN $500-$2,000/MONTH
COOKING FROM HOME?

Join Lambalia as a home chef!
✓ Set your own rates
✓ Flexible schedule
✓ Only 10% commission
✓ Cook what you love

SIGN UP: lambalia.com/chef

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FOOD LOVER?

Order authentic home-cooked meals from:
🇳🇬 Nigeria • 🇲🇽 Mexico • 🇮🇳 India
🇮🇹 Italy • 🇹🇭 Thailand • + 75 more!

lambalia.com | lambalia.app

@lambalia
Instagram • TikTok • Facebook

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[QR CODE to lambalia.com]
```

---

## **Where to Order Custom Bags:**

**Online Printing Services:**
1. **Vistaprint** - vistaprint.com
   - 150 custom bags: ~$60-80
   - 5-7 day shipping

2. **PackagingSupplies.com**
   - 150 custom bags: ~$50-70
   - Bulk pricing available

3. **Local Champaign Printer:**
   - FastSigns Champaign: (217) 355-5200
   - Get quote for 150 custom bags

---

# 📋 CAMPAIGN LOGISTICS & COORDINATION

## **Timeline (3 Weeks Out):**

### **Week 1 (This Week):**
- [ ] Finalize date and time with 3 home chefs
- [ ] Create Google Form signup page
- [ ] Design flyers and bags
- [ ] Order custom bags (5-7 day lead time)
- [ ] Contact WDWS Radio to book ad spots
- [ ] Calculate total ingredient costs
- [ ] Purchase ingredients (or schedule purchase for Week 3)

### **Week 2:**
- [ ] Print 400 flyers
- [ ] Distribute flyers around Champaign
- [ ] Launch radio campaign (starts Monday Week 2)
- [ ] Social media announcement (Instagram, Facebook, TikTok)
- [ ] Post in local Facebook groups
- [ ] Post on University of Illinois subreddit
- [ ] Email to friends/family/network
- [ ] Monitor signups daily

### **Week 3 (Event Week):**
- [ ] Monday: Check signup count (hopefully close to 150!)
- [ ] Tuesday: Close signups if 150 reached
- [ ] Wednesday: Finalize pickup schedule, assign times
- [ ] Thursday: Deliver ingredients to 3 home chefs
- [ ] Friday: Chefs prep (marinate chicken, prep spices)
- [ ] **SATURDAY: EVENT DAY!**

---

## **Chef Coordination System:**

### **Assign Meals Equally:**

Each chef gets 50 meals distributed across time slots:

**Chef A Location: [Address]**
- 12:00-2:00 PM: Codes LAMB-0001-A through LAMB-0017-A
- 2:00-4:00 PM: Codes LAMB-0018-A through LAMB-0033-A
- 4:00-6:00 PM: Codes LAMB-0034-A through LAMB-0050-A

**Chef B Location: [Address]**
- 12:00-2:00 PM: Codes LAMB-0051-B through LAMB-0067-B
- 2:00-4:00 PM: Codes LAMB-0068-B through LAMB-0083-B
- 4:00-6:00 PM: Codes LAMB-0084-B through LAMB-0100-B

**Chef C Location: [Address]**
- 12:00-2:00 PM: Codes LAMB-0101-C through LAMB-0117-C
- 2:00-4:00 PM: Codes LAMB-0118-C through LAMB-0133-C
- 4:00-6:00 PM: Codes LAMB-0134-C through LAMB-0150-C

---

### **Chef Checklist (Provide to Each Chef):**

```
LAMBALIA FREE MEAL LAUNCH - CHEF GUIDE

YOUR ASSIGNMENT: 50 meals
YOUR CODES: LAMB-XXXX-[Your Letter]

PICKUP DAY: Saturday, [DATE]
YOUR LOCATION: [Your Address]
HOURS: 12 PM - 6 PM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MEAL COMPONENTS (per serving):
✓ Jollof Rice (1 cup cooked)
✓ Fried Chicken (2 pieces)
✓ Fried Plantains (3-4 slices)

PACKAGING:
✓ Use provided Lambalia bags
✓ Include napkins and fork
✓ Seal bag securely

VERIFICATION PROCESS:
1. Customer shows you their code (phone or paper)
2. Check code matches your letter (A, B, or C)
3. Find code on your list, mark as "Picked Up"
4. Hand them their meal
5. Thank them and encourage app signup!

TALKING POINTS:
"Thanks for trying Lambalia! Did you know you can order more meals like this through our app? Just visit lambalia.com!"

QUESTIONS?
Call/Text Issa: [YOUR PHONE]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PAYMENT:
You'll receive [$ amount] after event completion.
Payment via [Venmo/Zelle/Cash].

Thank you for making this launch successful! 💚
```

---

# 💰 BUDGET BREAKDOWN

## **Estimated Costs:**

**Ingredients (150 meals):**
- Rice (30 lbs): $30
- Chicken (75 lbs): $150
- Plantains (150 count): $75
- Spices, tomatoes, peppers, oil, etc.: $100
- **Subtotal: ~$355**

**Marketing Materials:**
- Custom bags (150): $75
- Flyers (400): $40
- **Subtotal: ~$115**

**Chef Payment:**
- 3 chefs × $150 each = $450
- (Or negotiate based on their preference)

**Radio Advertising:**
- WDWS spots (70 total): ~$500-800
- (Negotiate package deal)

**Miscellaneous:**
- Napkins, forks, extras: $30
- Gas/transportation: $20

**TOTAL ESTIMATED COST: $1,470 - $1,770**

---

## **Cost-Saving Tips:**

1. **Negotiate Radio Bundle:**
   - Ask for "new business discount"
   - Offer to mention WDWS in social media posts
   - Target: $500 for entire 2-week campaign

2. **Partner with Local Grocer:**
   - Approach Champaign grocery stores for ingredient sponsorship
   - Offer to mention them: "Ingredients provided by [Store Name]"

3. **University Partnership:**
   - Contact UIUC International Student Services
   - Offer as cultural event - might get funding support

4. **Chamber of Commerce:**
   - Ask Champaign Chamber to co-promote
   - Might get discounted/free radio spots as member benefit

---

# 📊 SUCCESS METRICS TO TRACK

**During Campaign:**
- [ ] Number of signups (goal: 150)
- [ ] Time to reach 150 (faster = more demand)
- [ ] Radio ad effectiveness (ask signups "How did you hear about us?")
- [ ] Social media engagement
- [ ] Flyer scan rate (QR code tracking)

**Event Day:**
- [ ] Actual pickup rate (goal: 90%+ show up)
- [ ] No-show rate
- [ ] Customer feedback (have feedback forms)
- [ ] New app signups during event
- [ ] Email list growth

**Post-Event:**
- [ ] How many free meal recipients become paying customers?
- [ ] Social media mentions/tags
- [ ] Word-of-mouth referrals
- [ ] Media coverage (local newspaper pickup?)

---

# 📸 EVENT DAY DOCUMENTATION

**Content to Capture:**

**Photos:**
- [ ] Food preparation (chefs cooking)
- [ ] Packaged meals in Lambalia bags
- [ ] Happy customers receiving meals
- [ ] Customers showing their unique codes
- [ ] Group photo with 3 home chefs
- [ ] Before/after (empty table → empty bags)

**Videos:**
- [ ] Time-lapse of pickup line
- [ ] Customer testimonials (ask permission)
- [ ] Chef preparing meals (behind the scenes)
- [ ] "Thank you" video for social media

**Use This Content For:**
- Instagram/TikTok posts
- Future marketing campaigns
- Press kit for media
- Website testimonials
- Case study: "How we launched in Champaign"

---

# 🎯 POST-EVENT FOLLOW-UP

## **Day After Event:**

**Email to All 150 Participants:**

```
Subject: Thanks for Trying Lambalia! Here's 20% Off Your First Order

Hi [NAME],

Thank you for joining us at yesterday's Lambalia Free Meal Launch! We hope you enjoyed your Nigerian Jollof Rice. 🍗🍚

SPECIAL OFFER - JUST FOR YOU:
Get 20% OFF your first order on Lambalia
Use code: LAUNCH20

Ready to order? Visit lambalia.com

WHY ORDER THROUGH LAMBALIA?
✓ Authentic home-cooked meals
✓ 80+ countries represented
✓ Support local home chefs
✓ Delivered to your door

Want to become a chef and earn $500-$2,000/month?
Visit: lambalia.com/chef

Thanks again!
Issa Issantu
Founder, Lambalia

P.S. - We'd love your feedback! Reply to this email and let us know what you thought of your meal.
```

---

## **Week After Event:**

- [ ] Send follow-up to no-shows (offer makeup opportunity)
- [ ] Share event photos on social media
- [ ] Thank the 3 home chefs publicly (tag them)
- [ ] Write blog post: "How We Launched Lambalia in Champaign"
- [ ] Submit story to local media (News-Gazette, Smile Politely)
- [ ] Calculate conversion rate (free meal → paying customer)
- [ ] Plan next campaign based on learnings

---

# ✅ MASTER CHECKLIST

## **3 Weeks Before:**
- [ ] Confirm 3 home chefs availability
- [ ] Set exact date and time
- [ ] Calculate ingredient quantities
- [ ] Create Google Form signup
- [ ] Design flyers
- [ ] Design takeaway bags
- [ ] Book radio ad slots with WDWS

## **2 Weeks Before:**
- [ ] Order custom bags (150)
- [ ] Print flyers (400)
- [ ] Launch radio campaign
- [ ] Distribute flyers around Champaign
- [ ] Post on social media (Instagram, TikTok, Facebook)
- [ ] Post in local Facebook groups & UIUC subreddit
- [ ] Send email blast to network

## **1 Week Before:**
- [ ] Monitor signup count daily
- [ ] Close signups at 150 (or extend if needed)
- [ ] Assign pickup times to each code
- [ ] Send final confirmation emails with pickup details
- [ ] Create chef assignment lists
- [ ] Print chef checklists (3 copies)
- [ ] Purchase all ingredients

## **3 Days Before:**
- [ ] Deliver ingredients to 3 home chefs
- [ ] Provide bags, napkins, forks to chefs
- [ ] Confirm pickup locations with chefs
- [ ] Test run: cook 1 sample meal
- [ ] Finalize pickup logistics

## **Event Day (Saturday):**
- [ ] Arrive early to help setup
- [ ] Bring: extra bags, napkins, printed code lists, camera
- [ ] Document everything (photos/videos)
- [ ] Collect customer feedback
- [ ] Handle any issues (wrong code, missing signup, etc.)
- [ ] Thank chefs and participants
- [ ] Pay chefs

## **After Event:**
- [ ] Send thank you email to all participants
- [ ] Share content on social media
- [ ] Write press release for local media
- [ ] Pay chefs (if not done day-of)
- [ ] Calculate metrics and ROI
- [ ] Plan next campaign

---

**YOUR CAMPAIGN STRATEGY IS COMPLETE!**

**Next Steps:**
1. Set exact date (which Saturday?)
2. Confirm 3 home chefs
3. Create Google Form (I can help with exact setup)
4. Design flyers (want me to create copy?)
5. Contact WDWS Radio for ad pricing

Let me know which part you want to tackle first! 🚀🍽️
