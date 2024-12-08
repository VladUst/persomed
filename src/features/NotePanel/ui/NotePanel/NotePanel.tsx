import {
  Divider,
  ListItemIcon,
  ListItemText,
  MenuItem,
  MenuList,
} from "@mui/material";
import { useState } from "react";
import { classNames } from "@/shared/lib/classNames";
import cls from "./NotePanel.module.scss";
import {
  DescriptionOutlined,
  MedicalInformationOutlined,
} from "@mui/icons-material";
import { AnamnesisForm } from "../InfoForm/AnamnesisForm";
import { RecommendationsForm } from "../InfoForm/RecommendationsForm";

interface NotePanelProps {
  className?: string;
}

export const NotePanel = (props: NotePanelProps) => {
  const { className } = props;

  const [isAnamnesisFormOpen, setIsAnamnesisFormOpen] = useState(false);
  const [isRecommendationsFormOpen, setIsRecommendationsFormOpen] =
    useState(false);

  const showAnamnesisForm = () => {
    setIsAnamnesisFormOpen(true);
  };

  const closeAnamnesisForm = () => {
    setIsAnamnesisFormOpen(false);
  };

  const showRecommendationsForm = () => {
    setIsRecommendationsFormOpen(true);
  };

  const closeRecommendationsForm = () => {
    setIsRecommendationsFormOpen(false);
  };

  return (
    <div className={classNames(cls.NotePanel, {}, [className])}>
      <MenuList>
        <MenuItem onClick={showAnamnesisForm}>
          <ListItemIcon>
            <DescriptionOutlined fontSize="small" />
          </ListItemIcon>
          <ListItemText>Сохранить анамнез</ListItemText>
        </MenuItem>
        <Divider />
        <MenuItem onClick={showRecommendationsForm}>
          <ListItemIcon>
            <MedicalInformationOutlined fontSize="small" />
          </ListItemIcon>
          <ListItemText>Составить рекомендации</ListItemText>
        </MenuItem>
      </MenuList>
      <AnamnesisForm
        isOpen={isAnamnesisFormOpen}
        onClose={closeAnamnesisForm}
      />
      <RecommendationsForm
        isOpen={isRecommendationsFormOpen}
        onClose={closeRecommendationsForm}
      />
    </div>
  );
};
