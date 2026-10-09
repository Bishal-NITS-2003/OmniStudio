import React from 'react';
import { Search, Compass, FileText, Video, ShieldCheck, UserCheck, Send } from 'lucide-react';

interface StepperProgressProps {
  currentStep: string;
  status: string;
}

const STEPS = [
  { id: 'analyze_product', label: '1. Analysis', icon: Search },
  { id: 'plan_campaign', label: '2. Storyboard', icon: Compass },
  { id: 'generate_content', label: '3. Social Copy', icon: FileText },
  { id: 'quality_check', label: '4. Quality Audit', icon: ShieldCheck },
  { id: 'generate_media', label: '5. Parallel Media', icon: Video },
  { id: 'human_approval', label: '6. Review Gate', icon: UserCheck },
  { id: 'publish_parallel', label: '7. Parallel Publish', icon: Send },
];

export const StepperProgress: React.FC<StepperProgressProps> = ({ currentStep, status }) => {
  const getStepIndex = (step: string) => {
    if (step === 'generate_poster' || step === 'generate_video' || step === 'generate_media' || step === 'assemble_media') return 4;
    if (step === 'quality_check') return 3;
    if (step === 'human_approval') return 5;
    if (step === 'publish' || step === 'publish_parallel') return 6;
    if (status === 'PUBLISHED') return 6;
    if (status === 'WAITING_APPROVAL') return 5;
    const idx = STEPS.findIndex(s => s.id === step);
    if (idx !== -1) return idx;
    if (step === 'starting' || step === 'draft' || step === 'created') return 0;
    return 0;
  };

  const activeIndex = getStepIndex(currentStep);
  const isFinished = status === 'PUBLISHED';

  return (
    <div className="pipeline-stepper">
      <div className="stepper-line" />
      <div
        className="stepper-line-active"
        style={{
          width: `${(activeIndex / (STEPS.length - 1)) * 100}%`
        }}
      />

      {STEPS.map((step, index) => {
        const Icon = step.icon;
        const isCompleted = index < activeIndex || isFinished;
        const isCurrent = index === activeIndex && !isFinished;

        return (
          <div
            key={step.id}
            className={`step-node ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''}`}
          >
            <div className="step-circle">
              <Icon size={20} />
            </div>
            <span className="step-label">{step.label}</span>
          </div>
        );
      })}
    </div>
  );
};
