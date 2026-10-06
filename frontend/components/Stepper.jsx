'use client';

import React,{useState,Children,useRef,useLayoutEffect} from 'react';
import {motion,AnimatePresence} from 'motion/react';
import './Stepper.css';

export default function Stepper({children,initialStep=1,onStepChange=()=>{},onFinalStepCompleted=()=>{},stepCircleContainerClassName='',stepContainerClassName='',contentClassName='',footerClassName='',backButtonProps={},nextButtonProps={},backButtonText='Back',nextButtonText='Continue',disableStepIndicators=false,renderStepIndicator,...rest}){
 const [currentStep,setCurrentStep]=useState(initialStep),[direction,setDirection]=useState(0);
 const stepsArray=Children.toArray(children),totalSteps=stepsArray.length,isCompleted=currentStep>totalSteps,isLastStep=currentStep===totalSteps;
 const updateStep=newStep=>{setCurrentStep(newStep);newStep>totalSteps?onFinalStepCompleted():onStepChange(newStep)};
 const go=delta=>{setDirection(delta>0?1:-1);updateStep(currentStep+delta)};
 return <div className="saathi-stepper" {...rest}>
  <div className={`step-circle-container ${stepCircleContainerClassName}`.trim()}>
   <div className={`step-indicator-row ${stepContainerClassName}`.trim()}>
    {stepsArray.map((_,index)=>{const step=index+1;return <React.Fragment key={step}>
     {renderStepIndicator?renderStepIndicator({step,currentStep,onStepClick:clicked=>{setDirection(clicked>currentStep?1:-1);updateStep(clicked)}}):<StepIndicator step={step} currentStep={currentStep} disableStepIndicators={disableStepIndicators} onClickStep={clicked=>{setDirection(clicked>currentStep?1:-1);updateStep(clicked)}}/>}
     {index<totalSteps-1&&<StepConnector isComplete={currentStep>step}/>}
    </React.Fragment>})}
   </div>
   <StepContentWrapper isCompleted={isCompleted} currentStep={currentStep} direction={direction} className={contentClassName}>{stepsArray[currentStep-1]}</StepContentWrapper>
   {!isCompleted&&<div className={`footer-container ${footerClassName}`.trim()}><div className={`footer-nav ${currentStep!==1?'spread':'end'}`}>{currentStep!==1&&<button type="button" onClick={()=>go(-1)} className="back-button" {...backButtonProps}>{backButtonText}</button>}<button type="button" onClick={()=>isLastStep?updateStep(totalSteps+1):go(1)} className="next-button" {...nextButtonProps}>{isLastStep?'Complete':nextButtonText}</button></div></div>}
  </div>
 </div>;
}
function StepContentWrapper({isCompleted,currentStep,direction,children,className}){const [height,setHeight]=useState(0);return <motion.div className={`step-content-default ${className||''}`.trim()} animate={{height:isCompleted?0:height}} transition={{type:'spring',duration:.4}}><AnimatePresence initial={false} mode="sync" custom={direction}>{!isCompleted&&<SlideTransition key={currentStep} direction={direction} onHeightReady={setHeight}>{children}</SlideTransition>}</AnimatePresence></motion.div>}
function SlideTransition({children,direction,onHeightReady}){const ref=useRef(null);useLayoutEffect(()=>{if(ref.current)onHeightReady(ref.current.offsetHeight)},[children,onHeightReady]);return <motion.div ref={ref} custom={direction} variants={variants} initial="enter" animate="center" exit="exit" transition={{duration:.4}} className="step-slide">{children}</motion.div>}
const variants={enter:(d)=>({x:d>=0?'-100%':'100%',opacity:0}),center:{x:'0%',opacity:1},exit:(d)=>({x:d>=0?'50%':'-50%',opacity:0})};
export function Step({children}){return <div className="step-default">{children}</div>}
function StepIndicator({step,currentStep,onClickStep,disableStepIndicators}){const status=currentStep===step?'active':currentStep<step?'inactive':'complete';return <motion.div onClick={()=>step!==currentStep&&!disableStepIndicators&&onClickStep(step)} className="step-indicator" animate={status} initial={false} style={disableStepIndicators?{pointerEvents:'none',opacity:.5}:undefined}><motion.div className="step-indicator-inner" variants={{inactive:{backgroundColor:'#e4e8e1',color:'#7a847c'},active:{backgroundColor:'#d9a64b',color:'#d9a64b'},complete:{backgroundColor:'#183d32',color:'#fff'}}} transition={{duration:.3}}>{status==='complete'?<CheckIcon/>:status==='active'?<div className="active-dot"/>:<span className="step-number">{step}</span>}</motion.div></motion.div>}
function StepConnector({isComplete}){return <div className="step-connector"><motion.div className="step-connector-inner" initial={false} animate={isComplete?'complete':'incomplete'} variants={{incomplete:{width:0,backgroundColor:'transparent'},complete:{width:'100%',backgroundColor:'#d9a64b'}}} transition={{duration:.4}}/></div>}
function CheckIcon(){return <svg className="check-icon" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><motion.path initial={{pathLength:0}} animate={{pathLength:1}} transition={{delay:.1,type:'tween',ease:'easeOut',duration:.3}} strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/></svg>}
