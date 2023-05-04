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
        DrawMatrix.size = nAttr.create('size', 'sz', OpenMaya.MFnNumericData.kFloat, 0)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # ベクトルの表示チェック
        DrawMatrix.bool = nAttr.create( 'bool', 'bl', OpenMaya.MFnNumericData.kBoolean)
        nAttr.writable = True
        nAttr.keyable = True

        # vetorアトリビュート
        DrawMatrix.setVec = nAttr.create('setVector', 'setv', OpenMaya.MFnNumericData.k3Float, 0.0)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True
        nAttr.array = True

        # アトリビュートをセットする
        DrawMatrix.addAttribute( DrawMatrix.size )
        DrawMatrix.addAttribute( DrawMatrix.bool )
        DrawMatrix.addAttribute( DrawMatrix.setVec)

        return True
        
        
#=========================================
class UserData( OpenMaya.MUserData ):

    #-----------------------------------------------
    def __init__( self ):
        OpenMaya.MUserData.__init__( self, False )
        self.matrix = []
        self.size = []
        self.bool = []
        self.vector = []
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
        #return OpenMayaRender.MRenderer.kDirectX11
        #OpenGLを使用して描画する
        return OpenMayaRender.MRenderer.kOpenGL
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
                newData.matrix = []
                newData.size = []
                newData.bool = []
                newData.vector = []
            else:
                newData = UserData()
            
            # 自身のロケータの情報を読み込む
            thisNode = objPath.node()
            fnNode = OpenMaya.MFnDependencyNode( thisNode )


            # worldMatrixアトリビュートの情報を取得
            plugs_mtrx = fnNode.findPlug("worldMatrix", True )
            plug_mtrx = plugs_mtrx.elementByLogicalIndex(0)
            omtrxdata = plug_mtrx.asMObject()
            mmtrxdata = OpenMaya.MFnMatrixData(omtrxdata)
            # matrixとして扱えるようにする
            mmtrx = mmtrxdata.matrix()
            newData.matrix.append(mmtrx)

            # boolアトリビュートの情報を取得
            boolPlug = fnNode.findPlug( 'bool', False ).asBool()
            newData.bool.append(boolPlug)

            # sizeアトリビュートの情報を取得
            typePlug = fnNode.findPlug( 'size', False ).asFloat()
            newData.size.append(typePlug)
            arry_data = fnNode.findPlug( 'setVector', False )
            arry_value = arry_data.numElements()
            #vec3として扱えるようにする
            for index in range(arry_value):
                elementPlug = arry_data.elementByPhysicalIndex(index)
                xvec = elementPlug.child(0).asFloat()
                yvec = elementPlug.child(1).asFloat()
                zvec = elementPlug.child(2).asFloat()
                newData.vector.append([xvec,yvec,zvec])
            return newData

        return None
    
    #-----------------------------------------------
    def addUIDrawables( self, objPath, drawManager, frameContext, data ):
        
        # 更新されたデータを取得
        matrix = data.matrix[0]
        value = data.size[0]
        bool = data.bool[0]
        vetor = data.vector

        # matrixの描画処理   
        # X軸
        drawManager.beginDrawable()
        color = OpenMaya.MColor([1.0,0.0,0.0])
        drawManager.setColor( color )
        drawManager.line(OpenMaya.MPoint(0.0,0.0,0.0,1),
        OpenMaya.MPoint(1.0+value,0.0,0.0,1)) 
        drawManager.endDrawable()

        # Y軸 
        drawManager.beginDrawable()
        color = OpenMaya.MColor([0.0,1.0,0.0])
        drawManager.setColor( color )
        drawManager.line(OpenMaya.MPoint(0.0,0.0,0.0,1),
        OpenMaya.MPoint(0.0,1.0+value,0.0,1)) 
        drawManager.endDrawable()

        # Z軸  
        drawManager.beginDrawable()
        color = OpenMaya.MColor([0.0,0.0,1.0])
        drawManager.setColor( color )
        drawManager.line(OpenMaya.MPoint(0.0,0.0,0.0,1),
        OpenMaya.MPoint(0.0,0.0,1.0+value,1))
        drawManager.endDrawable()

        # ベクトルの表示をしないなら処理をここで終わる
        if bool ==False:
            return
        # 入力されたベクトルの数だけラインを描画する
        for index in range(len(vetor)):

            # ベクトル情報をマトリクスに変換
            vec = vetor[index]
            locat_mat = OpenMaya.MMatrix(
            [1.0,0.0,0.0,0.0,
            0.0,1.0,0.0,0.0,
            0.0,0.0,1.0,0.0,
            vec[0],vec[1],vec[2],1.0]
            )    
            # 自身のマトリクスとかけ合わせて、移動してもベクトルが変化しないようにする
            trance = locat_mat * matrix.inverse()
            tra_mat = OpenMaya.MTransformationMatrix(trance)
            localvec = tra_mat.translation(OpenMaya.MSpace.kWorld)
            # ラインの描画処理
            drawManager.beginDrawable()
            color = OpenMaya.MColor([1.0,1.0,0.0])
            drawManager.setColor( color )
            drawManager.line(OpenMaya.MPoint(0.0,0.0,0.0,1),
            OpenMaya.MPoint(localvec[0],localvec[1],localvec[2],1)) 
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