import { useState, useCallback, useMemo } from "react";
import type { MedicalTerm, HighlightedSection } from "../model/types";
import { findMedicalTerms } from "../model/medicalTermsService";
import cls from "./MedicalTermsHighlighter.module.scss";
import { classNames } from "@/shared/lib/classNames";
import { TermDetailsPanel } from "./TermDetailsPanel";
import { Divider } from "@mui/material";

interface MedicalTermsHighlighterProps {
  sections: Record<string, string>;
  sectionTitles?: Record<string, string>;
  isActive: boolean;
  className?: string;
}

export const MedicalTermsHighlighter = (
  props: MedicalTermsHighlighterProps,
) => {
  const { sections, sectionTitles = {}, isActive, className } = props;
  const [selectedTerm, setSelectedTerm] = useState<MedicalTerm | null>(null);
  const [isDetailsPanelOpen, setIsDetailsPanelOpen] = useState(false);

  // Process sections to find medical terms
  const processedSections = useMemo(() => {
    return Object.entries(sections).map(([key, text]) => ({
      id: key,
      title: sectionTitles[key] || key,
      text,
      terms: isActive ? findMedicalTerms(text) : [],
      isHighlightMode: isActive,
    }));
  }, [sections, sectionTitles, isActive]);

  // Handle term click
  const handleTermClick = useCallback((term: MedicalTerm) => {
    setSelectedTerm(term);
    setIsDetailsPanelOpen(true);
  }, []);

  const handleClosePanel = useCallback(() => {
    setIsDetailsPanelOpen(false);
  }, []);

  // Render highlighter text with terms
  const renderHighlightedText = (section: HighlightedSection) => {
    if (!section.isHighlightMode || section.terms.length === 0) {
      return section.text;
    }

    const { text, terms } = section;
    const result = [];
    let lastIndex = 0;

    terms.forEach((term, index) => {
      // Add text before the term
      if (term.position.start > lastIndex) {
        result.push(text.substring(lastIndex, term.position.start));
      }

      // Add the term with highlighting
      const isSelected = selectedTerm?.id === term.id;
      result.push(
        <span
          key={`term-${index}`}
          className={classNames(
            cls.term,
            { [cls.highlighted]: true, [cls.selectedTerm]: isSelected },
            [],
          )}
          onClick={() => handleTermClick(term)}
          tabIndex={0}
          title={`${term.name} (${term.canonicalName})`}
          aria-label={`Медицинский термин: ${term.term} - ${term.canonicalName}`}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              handleTermClick(term);
            }
          }}
        >
          {term.term}
        </span>,
      );

      lastIndex = term.position.end;
    });

    // Add remaining text
    if (lastIndex < text.length) {
      result.push(text.substring(lastIndex));
    }

    return result;
  };

  return (
    <div className={classNames(cls.highlighter, {}, [className])}>
      {processedSections.map((section) => (
        <div key={section.id} className={cls.sectionContainer}>
          <Divider textAlign="left" className={cls.divider}>
            {section.title}
          </Divider>
          <div className={cls.textContainer}>
            {renderHighlightedText(section)}
          </div>
        </div>
      ))}

      <TermDetailsPanel
        term={selectedTerm}
        isOpen={isDetailsPanelOpen}
        onClose={handleClosePanel}
      />
    </div>
  );
};
