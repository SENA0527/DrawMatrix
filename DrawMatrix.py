# -*- coding: utf-8 -*-
import sys

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaRender as OpenMayaRender

def maya_useNewAPI():
    pass

#=========================================
class DrawMatrix( OpenMayaUI.MPxLocatorNode ):
    
    # ノードのアトリビュート名
    kPluginNodeTypeName = "DrawMatrix"
    
    #TypeIDを入れる
    NodeId = OpenMaya.MTypeId(0x80032)#ユニークID
    
    #オーバーライド用のID
    classfication = 'drawdb/geometry/DrawMatrix'
    registrantId = 'DrawMatrixPlugin'
    
    #-----------------------------------------------
    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)
    
    #-----------------------------------------------
    def draw( self, view, path, style, status ):
        pass
    
    #-----------------------------------------------
    def isBounded( self ):
        return True
    
    #-----------------------------------------------
    def boundingBox( self ):
    
        return OpenMaya.MBoundingBox( OpenMaya.MPoint( 1.0, 1.0, 1.0 ), 
        OpenMaya.MPoint( -1.0, -1.0, -1.0 ) )
    
    #-----------------------------------------------
    # creator
    @staticmethod
    def nodeCreator():
        return DrawMatrix()
    
    #-----------------------------------------------
    # initializer
    @staticmethod
    def nodeInitializer():

        # アトリビュートの種類の定義
        nAttr = OpenMaya.MFnNumericAttribute()

        # 形状変更用のアトリビュート
        DrawMatrix.input = nAttr.create('type', 'ty', OpenMaya.MFnNumericData.kFloat, 0)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # Rアトリビュート
        DrawMatrix.red = nAttr.create('startX', 'x', OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # Gアトリビュート
        DrawMatrix.green = nAttr.create('startY', 'y', OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # Bアトリビュート
        DrawMatrix.bleu = nAttr.create('startZ', 'z', OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # Rアトリビュート
        DrawMatrix.endx = nAttr.create('endX', 'ex', OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # Gアトリビュート
        DrawMatrix.endy = nAttr.create('endY', 'ey', OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # Bアトリビュート
        DrawMatrix.endz = nAttr.create('endZ', 'ez', OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True





        # アトリビュートをセットする
        DrawMatrix.addAttribute( DrawMatrix.input )
        DrawMatrix.addAttribute( DrawMatrix.red )
        DrawMatrix.addAttribute( DrawMatrix.green )
        DrawMatrix.addAttribute( DrawMatrix.bleu )
        DrawMatrix.addAttribute( DrawMatrix.endx )
        DrawMatrix.addAttribute( DrawMatrix.endy )
        DrawMatrix.addAttribute( DrawMatrix.endz )

        return True
        
        
#=========================================
class UserData( OpenMaya.MUserData ):

    #DrawMatrixに渡すデータ
    size = 0.0
    #-----------------------------------------------
    def __init__( self ):
        OpenMaya.MUserData.__init__( self, False )
        self.datas = []
        self.colorR = []
        self.colorG = []
        self.colorB = []
        self.endX = []
        self.endY = []
        self.endZ = []
#=========================================
class DrawMatrixOverride( OpenMayaRender.MPxDrawOverride ):
    
    #-----------------------------------------------
    def __init__( self, obj ):
        OpenMayaRender.MPxDrawOverride.__init__( self, obj, DrawMatrixOverride.draw )
    
    #-----------------------------------------------
    @staticmethod
    def draw( context, data ):
        pass
    
    #-----------------------------------------------
    def supportedDrawAPIs( self ):

        #DirectXを使用して描画する
        return OpenMayaRender.MRenderer.kDirectX11
        #OpenGLを使用して描画する
        #return OpenMayaRender.MRenderer.kOpenGL
    #-----------------------------------------------
    def hasUIDrawables( self ):
        return True
    
    #-----------------------------------------------
    def isBounded( self, objPath, cameraPath ):
        return True
    
    #-----------------------------------------------
    def boundingBox( self, objPath, cameraPath ):
    
        boxsize = 10000.0
        bbox = OpenMaya.MBoundingBox(OpenMaya.MPoint(boxsize, boxsize, boxsize),
        OpenMaya.MPoint(-boxsize, -boxsize, -boxsize))
    
        return bbox
    #-----------------------------------------------
    def disableInternalBoundingBoxDraw( self ):
        return True
    
    #-----------------------------------------------
    def prepareForDraw( self, objPath, cameraPath, frameContext, oldData ):

        # データ更新処理
        if( objPath ):
            newData = None
            if( oldData ):
                newData = oldData
                newData.datas = []
                newData.colorR = []
                newData.colorG = []
                newData.colorB = []
                newData.endX = []
                newData.endY = []
                newData.endZ = []


            else:
                newData = UserData()
            
            # 自身のロケータの情報を読み込む
            thisNode = objPath.node()
            fnNode = OpenMaya.MFnDependencyNode( thisNode )

            # typeアトリビュートの情報を取得
            typePlug = fnNode.findPlug( 'type', False ).asFloat()
            newData.datas.append(typePlug)
            
            #RGBの情報を取得
            colorPlugR = fnNode.findPlug( 'startX', False ).asFloat()
            newData.colorR.append(colorPlugR)
            colorPlugG = fnNode.findPlug( 'startY', False ).asFloat()
            newData.colorG.append(colorPlugG)
            colorPlugB = fnNode.findPlug( 'startZ', False ).asFloat()
            newData.colorB.append(colorPlugB)

            #RGBの情報を取得
            colorPlugR = fnNode.findPlug( 'endX', False ).asFloat()
            newData.endX.append(colorPlugR)
            colorPlugG = fnNode.findPlug( 'endY', False ).asFloat()
            newData.endY.append(colorPlugG)
            colorPlugB = fnNode.findPlug( 'endZ', False ).asFloat()
            newData.endZ.append(colorPlugB)
            return newData

        return None
    
    #-----------------------------------------------
    def addUIDrawables( self, objPath, drawManager, frameContext, data ):

        # ベースメッシュのデータが空でなければ、描画処理を実行する
        if data.datas != []:
        
            value = data.datas[0]
            color_r = data.colorR[0]
            color_g = data.colorG[0]
            color_b = data.colorB[0]
            ex = data.endX[0]
            ey = data.endY[0]
            ez = data.endZ[0]
            # ボックスの描画処理   
            drawManager.beginDrawable()
            color = OpenMaya.MColor([1.0,1.0,0.0])
            drawManager.setColor( color )
            #box
            drawManager.line(
   
            OpenMaya.MPoint(color_r ,color_g,color_b,1),
            OpenMaya.MPoint(ex,ey,ez,1)
            ) # ←表示されるボックスのサイズ
            drawManager.endDrawable()



            # ボックスの描画処理   
            drawManager.beginDrawable()
            color = OpenMaya.MColor([1.0,0.0,0.0])
            drawManager.setColor( color )
            #box
            drawManager.line(
            OpenMaya.MPoint(0.0,0.0,0.0,1),
            OpenMaya.MPoint(1.0+value,0.0,0.0,1)
            ) # ←表示されるボックスのサイズ
            drawManager.endDrawable()

            # ボックスの描画処理   
            drawManager.beginDrawable()
            color = OpenMaya.MColor([0.0,1.0,0.0])
            drawManager.setColor( color )
            #box
            drawManager.line(
            OpenMaya.MPoint(0.0,0.0,0.0,1),
            OpenMaya.MPoint(0.0,1.0+value,0.0,1)
            ) # ←表示されるボックスのサイズ
            drawManager.endDrawable()

            # ボックスの描画処理   
            drawManager.beginDrawable()
            color = OpenMaya.MColor([0.0,0.0,1.0])
            drawManager.setColor( color )
            #box
            drawManager.line(
            OpenMaya.MPoint(0.0,0.0,0.0,1),
            OpenMaya.MPoint(0.0,0.0,1.0+value,1)
            ) # ←表示されるボックスのサイズ
            drawManager.endDrawable()



        return True
    
    #-----------------------------------------------
    @staticmethod
    def creator( obj ):
        return DrawMatrixOverride( obj )
    
#-----------------------------------------------
# initialize
def initializePlugin( obj ):
    
    mplugin = OpenMaya.MFnPlugin( obj, "DrawMatrix", "3.0", "Any" )
    try:
        mplugin.registerNode( DrawMatrix.kPluginNodeTypeName, DrawMatrix.NodeId, 
        DrawMatrix.nodeCreator, DrawMatrix.nodeInitializer, OpenMaya.MPxNode.kLocatorNode,
        DrawMatrix.classfication )

        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator( DrawMatrix.classfication,
        DrawMatrix.registrantId,DrawMatrixOverride.creator )
    													  
    except:
        sys.stderr.write( "Failed to register node: %s" % DrawMatrix.kPluginNodeTypeName )
        raise
    
#-----------------------------------------------
# uninitialize
def uninitializePlugin( obj ):
    
    mplugin = OpenMaya.MFnPlugin( obj, "DrawMatrix", "3.0", "Any" )
    try:
        mplugin.deregisterNode( DrawMatrix.NodeId )
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator( DrawMatrix.classfication,
        DrawMatrix.registrantId )
    except:
        sys.stderr.write( "Failed to deregister node: %s" % DrawMatrix.kPluginNodeTypeName )
        raise