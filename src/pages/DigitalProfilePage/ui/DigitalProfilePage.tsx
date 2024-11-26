import {
  AllergiesInfo,
  DetailedInfo,
  FamilyInfo,
  GeneralInfo,
  LifestyleInfo,
  PreventiveInfio,
} from "@/features/PatientStateInfo";
import { Page } from "@/widgets/Page";

export const DigitalProfilePage = () => {
  return (
    <Page>
      <GeneralInfo />
      <DetailedInfo />
      <PreventiveInfio />
      <AllergiesInfo />
      <FamilyInfo />
      <LifestyleInfo />
    </Page>
  );
};
