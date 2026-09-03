import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  Video,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { z } from "zod";
import { loadFont } from "@remotion/google-fonts/NotoSansKR";

// Load Noto Sans KR font for Korean subtitles
const { fontFamily } = loadFont("normal", {
  weights: ["700", "900"],
});

// Define schema for parameterized rendering
export const dynamicVideoSchema = z.object({
  folderName: z.string(),
  videoFileName: z.string().optional(),
  audioFileName: z.string().optional(),
  disableAudio: z.boolean().optional(),
  sceneData: z.array(
    z.object({
      scene_id: z.number(),
      start: z.number(),
      end: z.number(),
      duration_frames: z.number(),
      has_video: z.boolean().optional(),
      text_blocks: z.array(
        z.object({
          text: z.string(),
          start: z.number(),
          end: z.number(),
        })
      ),
    })
  ),
  durationInFrames: z.number(),
});

type DynamicVideoProps = z.infer<typeof dynamicVideoSchema>;

// Subtitle Overlay component
const SubtitleOverlay: React.FC<{
  sceneData: DynamicVideoProps["sceneData"];
}> = ({ sceneData }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // Flatten all text blocks across all scenes to check against global time
  const allBlocks = sceneData.flatMap((scene) => scene.text_blocks);

  // Find the active text block for the current timestamp
  const currentBlock = allBlocks.find(
    (block) => currentTime >= block.start && currentTime <= block.end
  );

  if (!currentBlock) {
    return null;
  }

  return (
    <div
      style={{
        position: "absolute",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        width: "90%",
        textAlign: "center",
        zIndex: 10,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          fontFamily,
          fontSize: "63px",
          fontWeight: 900,
          color: "#FFFFFF",
          textShadow: `
            -4px -4px 0 #000,  
             4px -4px 0 #000,
            -4px  4px 0 #000,
             4px  4px 0 #000,
             0px  5px 12px rgba(0, 0, 0, 0.9)
          `,
          backgroundColor: "rgba(0, 0, 0, 0.45)",
          padding: "16px 28px",
          borderRadius: "20px",
          display: "inline-block",
          lineHeight: 1.3,
          wordBreak: "keep-all",
          letterSpacing: "-1px",
        }}
      >
        {currentBlock.text}
      </div>
    </div>
  );
};

// Scene Video Component with graceful fallback
const SceneVideo: React.FC<{
  folderName: string;
  sceneId: number;
  hasVideo: boolean;
}> = ({ folderName, sceneId, hasVideo }) => {
  const videoSrc = staticFile(`outputs/${folderName}/scene${sceneId}.mp4`);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        background: "linear-gradient(135deg, #1e1e2f 0%, #11111b 100%)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {hasVideo ? (
        <Video
          src={videoSrc}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
          muted
          loop
        />
      ) : null}
    </div>
  );
};

export const DynamicVideo: React.FC<DynamicVideoProps> = ({
  folderName,
  videoFileName,
  audioFileName,
  disableAudio,
  sceneData,
}) => {
  const actualAudioFile = audioFileName || "output_1.2x.wav";
  const audioSrc = staticFile(`outputs/${folderName}/${actualAudioFile}`);
  const singleVideoSrc = videoFileName
    ? staticFile(`outputs/${folderName}/${videoFileName}`)
    : null;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {/* 1. Background Video Layer */}
      {singleVideoSrc ? (
        // 단일 비디오 모드 (예: video.mov / video.mp4)
        <Video
          src={singleVideoSrc}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
          muted={!disableAudio}
        />
      ) : (
        // 씬별 분할 비디오 모드
        sceneData.map((scene, index) => {
          const startFrame =
            index === 0 ? 0 : Math.round(sceneData[index - 1].end * 30);
          const endFrame = Math.round(scene.end * 30);
          const duration = endFrame - startFrame;

          return (
            <Sequence
              key={scene.scene_id}
              from={startFrame}
              durationInFrames={duration}
            >
              <SceneVideo
                folderName={folderName}
                sceneId={scene.scene_id}
                hasVideo={scene.has_video || false}
              />
            </Sequence>
          );
        })
      )}

      {/* 2. Combined Background Audio Track (나레이션) */}
      {!disableAudio && folderName && <Audio src={audioSrc} />}

      {/* 3. Global Subtitles Overlay */}
      <SubtitleOverlay sceneData={sceneData} />
    </AbsoluteFill>
  );
};
