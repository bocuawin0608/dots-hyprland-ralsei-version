import QtQuick
import QtQuick.Layouts
import QtQuick.Effects
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import qs.services
import qs.modules.common
import qs.modules.common.widgets

PanelWindow {
    id: root
    visible: GlobalStates.subtitleModeOpen
    color: "transparent"
    
    exclusionMode: ExclusionMode.Ignore
    exclusiveZone: 0
    anchors {
        bottom: true
        horizontalCenter: true
    }
    margins.bottom: Appearance.sizes.barHeight + 40
    
    WlrLayershell.namespace: "quickshell:subtitle"
    WlrLayershell.layer: WlrLayer.Overlay
    
    // Cava integration for music-reactiveness
    Process {
        id: cavaProc
        running: GlobalStates.subtitleModeOpen
        command: ["cava", "-p", `${FileUtils.trimFileProtocol(Directories.scriptPath)}/cava/raw_output_config.txt`]
        stdout: SplitParser {
            onRead: data => {
                let points = data.split(";").map(p => parseFloat(p.trim())).filter(p => !isNaN(p));
                // Simple average for reactiveness
                let avg = points.reduce((a, b) => a + b, 0) / Math.max(1, points.length);
                root.musicIntensity = avg / 1000.0; 
            }
        }
    }
    
    property real musicIntensity: 0.0
    property string currentSubtitle: "..." // Would be populated by an external subtitle scraper
    
    implicitWidth: subtitleContainer.implicitWidth
    implicitHeight: subtitleContainer.implicitHeight
    
    Rectangle {
        id: subtitleContainer
        color: ColorUtils.transparentize(Appearance.colors.colMagicContainer, 0.7)
        radius: Appearance.rounding.normal
        border.color: Appearance.colors.colMagic
        border.width: 1
        
        implicitWidth: Math.max(400, textLayout.implicitWidth + 40)
        implicitHeight: textLayout.implicitHeight + 20
        
        // Music-reactive scale and glow
        scale: 1.0 + (root.musicIntensity * 0.05)
        Behavior on scale {
            NumberAnimation { duration: 100 }
        }
        
        layer.enabled: true
        layer.effect: MultiEffect {
            source: subtitleContainer
            shadowEnabled: true
            shadowColor: Appearance.colors.colMagic
            shadowBlur: 1.0 + (root.musicIntensity * 2.0)
            shadowOpacity: 0.5 + (root.musicIntensity * 0.5)
        }
        
        RowLayout {
            id: textLayout
            anchors.centerIn: parent
            
            StyledText {
                text: root.currentSubtitle
                color: Appearance.colors.colLayer0 // "soft cream text" relative to dark background
                font.pixelSize: Appearance.font.pixelSize.huge
                font.bold: true
                wrapMode: Text.WordWrap
                Layout.maximumWidth: 800
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
    
    IpcHandler {
        target: "subtitle"
        function toggle(): void {
            GlobalStates.subtitleModeOpen = !GlobalStates.subtitleModeOpen;
        }
    }
}
