// @flow

import React from 'react';
import SplashScreen, {HeroImage} from "../componentsBySection/FindProjects/SplashScreen.jsx";
import RecentProjectsSection from "../componentsBySection/Landing/RecentProjectsSection.jsx";
import cdn from "../utils/cdn";
import Button from "react-bootstrap/Button";
import url from "../utils/url";
import Section from "../enums/Section";

class LandingController extends React.PureComponent<{||}> {

  constructor(): void {
    super();
  }

  render(): React$Node {
    return (
      <div className="FindProjectsController-root">
        <div className="container-fluid">
          {this._renderTopSplash()}
        </div>
        <div className="container">
          <RecentProjectsSection/>
          {this._renderPathFlows()}
          {this._renderPartnerSection()}
          {this._renderBottomSplash()}
        </div>
      </div>
    );
  }

  _renderTopSplash(): React$Node {
    const header: string = "Make Tech.  Do Good.";
    const text: string = "We connect skilled volunteers and tech-for-good projects";
    const buttonSection: string = "landingtop";

    return (
      <SplashScreen header={header} text={text} img={HeroImage.TopLanding} buttonSection={buttonSection}/>
    );
  }

  _renderPathFlows() {
    return (
      <div className="LandingController-pathflows row">
        <div className="col-xs-12 col-lg-6 LandingController-volunteer-flow">
          <h3>Want to Volunteer?</h3>
          <p>Apply your tech skills to projects that need them

            1. Create a Profile
            2. Search Projects
            3. Connect with Project Leaders</p>
            <Button variant="outline-primary">Start Volunteering!</Button>

          </div>
          <div className="col-xs-12 col-lg-6 LandingController-recruit-flow">
            <h3>Need Volunteers?</h3>
            <p>Find people with the tech skills you need

              1. Add your organization
              2. List your project needs
              3. Find skilled volunteers</p>
              <Button variant="primary">Start Recruiting!</Button>

            </div>
          </div>
        )
      }

      _renderPartnerSection() {
        return (
          <div className="about-us-vision" style={cdn.bgImage('OurVisionBGoverlay.jpg')}>
            <div className="PartnerSection">
              <h2>Partner With Us to Organize your Next Hackathon</h2>
              <p>DemocracyLab is the leading organizer for Tech-for-Good Hackathons.</p>
              <p>Let us help your company, non-profit or group organize your next Hackathon.</p>
              <Button variant="primary" className="SplashScreen-create-project-btn" href={url.sectionOrLogIn(Section.PartnerWithUs)}>
                Learn More
              </Button>
            </div>
          </div>
        )
      }

  _renderBottomSplash(): React$Node {
    const header: string = "What are you waiting for?";
    const buttonSection: string = "landingbottom";

    return (
      <SplashScreen header={header} img={HeroImage.BottomLanding} buttonSection={buttonSection}/>
    );
  }

}
export default LandingController;
