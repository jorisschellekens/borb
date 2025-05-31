import unittest

from borb.pdf import A4PortraitResume, Lipsum


class TestA4PortraitResume(unittest.TestCase):

    def test_a4_portrait_resume(self):
        (
            A4PortraitResume()
            .set_name("Alex Johnson")
            .set_about_me(
                "I'm a passionate problem solver and technology enthusiast. I enjoy tackling challenges, building innovative solutions, and playing strategy games in my spare time."
            )
            .set_picture("https://images.unsplash.com/photo-1499996860823-5214fcc65f8f")
            .append_honors_or_award("Employee of the Year - TechInnovate")
            .append_honors_or_award("Hackathon Winner - CodeFest 2023")
            .append_honors_or_award("Published in TechWorld Magazine")
            .append_language_and_proficiency("English", 5)
            .append_language_and_proficiency("Spanish", 4)
            .append_language_and_proficiency("German", 2)
            .append_language_and_proficiency("Mandarin", 1)
            .append_skill("3D Modeling")
            .append_skill("Digital Painting")
            .append_skill("Competitive Gaming")
            .set_email("alex.johnson.fake@gmail.com")
            .set_linkedin("alexjohnson_fakelinkedin")
            .set_twitter("alex_fake_twitter")
            .set_phone_nr("+1 555 123 4567")
            .set_location("Springfield, USA")
            .append_work_experience(
                company="TechInnovate Inc.",
                from_date="January 2023",
                to_date="Present",
                description="Leading a team of software engineers to develop AI-driven solutions for the retail industry. Implemented key product features that boosted client satisfaction by 30%.",
                tags=["python", "machine learning", "team leadership"],
            )
            .append_work_experience(
                company="InnoSoft Solutions",
                from_date="July 2019",
                to_date="December 2022",
                description="Developed and optimized web applications, improving load times by 50%. Collaborated with cross-functional teams to deliver projects on time.",
                tags=["javascript", "react", "devops"],
            )
            .append_work_experience(
                company="CodeBase Tech",
                from_date="May 2017",
                to_date="June 2019",
                description="Built scalable backend systems for e-commerce platforms. Enhanced database efficiency, reducing query response times by 40%.",
                tags=["java", "sql", "cloud computing"],
            )
        ).save("assets/test_a4_portrait_resume.pdf")
