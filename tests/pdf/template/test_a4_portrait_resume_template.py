from borb.pdf.template.a4_portrait_resume_template import A4PortraitResumeTemplate
from tests.test_case import TestCase


class TestA4PortraitResumeTemplate(TestCase):
    def test_a4_portrait_resume_template_001(self):
        A4PortraitResumeTemplate().set_name("John Doe").set_email(
            "john.doe@example.com"
        ).set_linkedin("linkedin.com/in/johndoe").set_location(
            "New York, NY"
        ).set_phone_nr(
            "+1 (123) 456-7890"
        ).set_twitter(
            "twitter.com/johndoe"
        ).set_profile_picture(
            "https://thispersondoesnotexist.com/"
        ).set_about_me(
            "A passionate software engineer with experience in full-stack web development and a strong focus on JavaScript technologies."
        ).add_work_experience(
            company_name="Tech Solutions Inc.",
            start_date="January 2019",
            end_date="Present",
            job_title="Full-Stack Developer",
            responsibilities=[
                "Developed and maintained web applications using React.js and Node.js",
                "Collaborated with cross-functional teams to deliver high-quality software solutions",
                "Participated in code reviews and contributed to improving coding standards",
            ],
        ).add_work_experience(
            company_name="Innovative Solutions Ltd.",
            start_date="June 2017",
            end_date="December 2018",
            job_title="Software Engineer",
            responsibilities=[
                "Designed and implemented RESTful APIs for a scalable web application",
                "Integrated third-party APIs for payment processing and user authentication",
                "Optimized database queries to improve application performance",
            ],
        ).add_work_experience(
            company_name="Digital Innovations Co.",
            start_date="September 2015",
            end_date="May 2017",
            job_title="Junior Developer",
            responsibilities=[
                "Developed front-end components using HTML, CSS, and JavaScript",
                "Assisted in debugging and troubleshooting issues in existing codebase",
                "Participated in Agile development processes and daily stand-up meetings",
            ],
        ).add_skill(
            "JavaScript"
        ).add_skill(
            "React.js"
        ).add_skill(
            "Node.js"
        ).add_skill(
            "HTML"
        ).add_skill(
            "CSS"
        ).add_skill(
            "Python"
        ).add_skill(
            "RESTful APIs"
        ).add_skill(
            "Agile"
        ).add_language_and_proficiency(
            "English", "Fluent"
        ).add_language_and_proficiency(
            "Spanish", "Intermediate"
        ).add_honor_or_award(
            "Dean's List, College of Engineering, 2018"
        ).add_interest(
            "Reading"
        ).add_interest(
            "Traveling"
        ).add_interest(
            "Hiking"
        ).save(
            self.get_first_output_file()
        )

    def test_a4_portrait_resume_template_002(self):
        A4PortraitResumeTemplate().set_name("Emily Smith").set_email(
            "emily.smith@example.com"
        ).set_linkedin("linkedin.com/in/emilysmith").set_profile_picture(
            "https://thispersondoesnotexist.com/"
        ).set_location(
            "Los Angeles, CA"
        ).set_phone_nr(
            "+1 (234) 567-8901"
        ).set_about_me(
            "A dedicated marketing professional with a passion for creating impactful campaigns and engaging with audiences. Experienced in developing marketing strategies, managing social media accounts, and analyzing market trends."
        ).add_work_experience(
            company_name="ABC Retail",
            start_date="January 2018",
            end_date="Present",
            job_title="Marketing Manager",
            responsibilities=[
                "Develop and execute marketing plans to increase brand awareness and drive sales",
                "Manage social media accounts and create engaging content for various platforms",
                "Conduct market research and analyze consumer behavior to identify trends and opportunities",
                "Collaborate with cross-functional teams to coordinate promotional events and campaigns",
            ],
        ).add_work_experience(
            company_name="XYZ Consulting",
            start_date="June 2015",
            end_date="December 2017",
            job_title="Marketing Specialist",
            responsibilities=[
                "Assist in the development and implementation of marketing strategies",
                "Create marketing collateral including brochures, flyers, and advertisements",
                "Coordinate with external vendors and agencies to execute marketing campaigns",
                "Monitor and report on the performance of marketing initiatives",
            ],
        ).add_work_experience(
            company_name="LMN Enterprises",
            start_date="February 2013",
            end_date="May 2015",
            job_title="Marketing Coordinator",
            responsibilities=[
                "Support the marketing team in planning and executing promotional activities",
                "Maintain and update marketing databases and customer mailing lists",
                "Assist in the organization of events such as trade shows and conferences",
                "Conduct competitive analysis and research on industry trends",
            ],
        ).add_skill(
            "Marketing"
        ).add_skill(
            "Social Media"
        ).add_skill(
            "Market Research"
        ).add_skill(
            "Events"
        ).add_skill(
            "Content"
        ).add_skill(
            "Adobe"
        ).add_language_and_proficiency(
            "English", "Native"
        ).add_language_and_proficiency(
            "Spanish", "Intermediate"
        ).add_honor_or_award(
            "Marketing Excellence Award, ABC Retail, 2020"
        ).add_interest(
            "Traveling"
        ).add_interest(
            "Photography"
        ).add_interest(
            "Yoga"
        ).save(
            self.get_second_output_file()
        )
